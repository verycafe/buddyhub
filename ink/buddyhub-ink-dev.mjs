#!/usr/bin/env node

import {spawnSync} from 'node:child_process';
import path from 'node:path';
import process from 'node:process';
import {fileURLToPath} from 'node:url';
import React, {useMemo, useState} from 'react';
import {render, Box, Text, useApp, useInput} from 'ink';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const PYTHON_TUI = path.join(ROOT, 'buddyhub_tui.py');

const TOP_LEVEL_LABELS = {
	language: 'Language',
	color: 'Color',
	nickname: 'Nickname',
	apply: 'Apply',
	restore: 'Restore',
	uninstall: 'Uninstall',
	quit: 'Quit'
};

const DETAILS = {
	language: 'Choose the BuddyHub menu language.',
	color: 'Choose a Buddy color preset. Preview updates instantly.',
	nickname: 'Type a new Buddy display name and save it into the working draft.',
	apply: 'Ink DEV prototype only. Real apply remains on the Python TUI today.',
	restore: 'Ink DEV prototype only. Real restore remains on the Python TUI today.',
	uninstall: 'Ink DEV prototype only. Real uninstall remains on the Python TUI today.',
	quit: 'Exit the Ink development prototype.'
};

const h = React.createElement;

function isEnter(input, key) {
	return Boolean(key.return || key.enter || input === '\n' || input === '\r');
}

function inkBox(props, ...children) {
	return h(Box, props, ...children.filter(Boolean));
}

function inkText(props, children) {
	return h(Text, props, children);
}

function sectionTitle(label) {
	return inkText({bold: true}, label);
}

function runPython(args) {
	const result = spawnSync('python3', [PYTHON_TUI, ...args], {
		cwd: ROOT,
		encoding: 'utf8'
	});

	if (result.error) {
		throw result.error;
	}

	if (result.status !== 0) {
		throw new Error((result.stderr || result.stdout || '').trim() || `python3 exited with ${result.status}`);
	}

	return JSON.parse(result.stdout);
}

function loadInitialData() {
	const state = runPython(['--dump-state']);
	const ui = runPython(['--dump-ui-model']);
	return {state, ui};
}

function topLevelValue(itemId, draft) {
	if (itemId === 'language') return draft.languageLabel;
	if (itemId === 'color') return draft.colorLabel || 'Default';
	if (itemId === 'nickname') return draft.nickname || draft.currentName || 'none';
	return '';
}

function menuRow(item, active) {
	return inkText(
		{color: active ? 'cyan' : undefined, bold: active},
		`${active ? '› ' : '  '}${TOP_LEVEL_LABELS[item]}`
	);
}

function optionRow(label, active, color) {
	return inkText(
		{color: active ? color || 'cyan' : color || undefined, bold: active},
		`${active ? '› ' : '  '}${label}`
	);
}

function previewCard(draft, currentVisual) {
	const previewName = draft.nickname || draft.currentName;
	const previewColor = draft.colorLabel || 'Default';
	const previewColorHex = draft.colorHex || '#c0c0c0';
	const previewLines = draft.previewLines.length > 0 ? draft.previewLines : ['(no preview)'];
	return inkBox(
		{flexDirection: 'column', borderStyle: 'round', borderColor: 'magenta', paddingX: 1, width: 56},
		sectionTitle('Preview'),
		inkBox(
			{flexDirection: 'column', marginTop: 1},
			inkText({color: 'gray'}, `Installed Buddy: ${currentVisual.name || 'Unknown'} / ${currentVisual.species || 'unknown'}`),
			inkText({color: 'gray'}, 'Preview updates as you browse color or type a nickname.'),
			inkText({bold: true, color: previewColorHex}, previewColor.toUpperCase()),
			inkText({bold: true}, previewName),
			inkText({color: 'gray'}, `Buddy: ${draft.species}`),
			...previewLines.map((line, index) => inkText({key: `preview-${index}`, color: previewColorHex}, line)),
			inkText({color: 'gray'}, `Element: ${draft.elementId || 'none'}`),
			inkText({color: 'gray'}, `Language: ${draft.languageLabel}`)
		)
	);
}

function selectionPanel(screen, uiModel, languageIndex, colorIndex, nicknameInput) {
	if (screen === 'language') {
		return inkBox(
			{marginTop: 1, flexDirection: 'column'},
			sectionTitle('Language Options'),
			...uiModel.languages.map((item, index) =>
				optionRow(item.label, index === languageIndex, index === languageIndex ? 'cyan' : undefined)
			)
		);
	}

	if (screen === 'color') {
		return inkBox(
			{marginTop: 1, flexDirection: 'column'},
			sectionTitle('Color Options'),
			...uiModel.colors.map((item, index) =>
				inkText(
					{
						key: item.color_id,
						color: index === colorIndex ? item.hex : 'gray',
						bold: index === colorIndex
					},
					`${index === colorIndex ? '› ' : '  '}${item.label}  ${item.hex}`
				)
			)
		);
	}

	if (screen === 'nickname') {
		return inkBox(
			{marginTop: 1, flexDirection: 'column'},
			sectionTitle('Nickname Input'),
			inkText({color: 'gray'}, 'Type a new name, then press Enter. Esc returns to the main menu.'),
			inkText({}, `Input: ${nicknameInput || '|'}`)
		);
	}

	return null;
}

function App({initialState, uiModel}) {
	const {exit} = useApp();
	const [screen, setScreen] = useState('main');
	const [mainIndex, setMainIndex] = useState(0);
	const [languageIndex, setLanguageIndex] = useState(() => {
		const current = initialState.settings.language_id;
		const index = uiModel.languages.findIndex(item => item.language_id === current);
		return index >= 0 ? index : 0;
	});
	const [colorIndex, setColorIndex] = useState(() => {
		const current = initialState.draft_visual.color_id;
		const index = uiModel.colors.findIndex(item => item.color_id === current);
		return index >= 0 ? index : 0;
	});
	const [nicknameInput, setNicknameInput] = useState('');
	const [savedNickname, setSavedNickname] = useState(initialState.settings.nickname || '');
	const [message, setMessage] = useState('Ink DEV prototype. Use arrows + Enter. Esc returns.');

	const currentVisual = initialState.current_visual || {};
	const draft = useMemo(() => {
		const color = uiModel.colors[colorIndex] || null;
		const language = uiModel.languages[languageIndex] || uiModel.languages[0];
		const effectiveNickname = screen === 'nickname' ? nicknameInput : savedNickname;

		return {
			languageId: language?.language_id || 'en',
			languageLabel: language?.label || 'English',
			colorId: color?.color_id || null,
			colorLabel: color?.label || null,
			colorHex: color?.hex || null,
			nickname: effectiveNickname || null,
			currentName: currentVisual.name || 'Unknown',
			species: currentVisual.species || 'unknown',
			previewLines: currentVisual.preview_lines || [],
			elementId: currentVisual.element_id || null
		};
	}, [colorIndex, currentVisual, languageIndex, nicknameInput, savedNickname, screen, uiModel.colors, uiModel.languages]);

	useInput((input, key) => {
		if (key.escape) {
			if (screen === 'main') {
				exit();
				return;
			}

			if (screen === 'nickname') {
				setNicknameInput('');
			}

			setScreen('main');
			setMessage('Returned to the main menu.');
			return;
		}

		if (input === 'q' && screen === 'main') {
			exit();
			return;
		}

		if (screen === 'main') {
			if (key.upArrow) {
				setMainIndex(index => (index - 1 + uiModel.top_level_menu.length) % uiModel.top_level_menu.length);
				return;
			}

			if (key.downArrow) {
				setMainIndex(index => (index + 1) % uiModel.top_level_menu.length);
				return;
			}

			if (isEnter(input, key)) {
				const itemId = uiModel.top_level_menu[mainIndex];
				if (itemId === 'language' || itemId === 'color' || itemId === 'nickname') {
					setScreen(itemId);
					if (itemId === 'nickname') {
						setNicknameInput('');
					}
					setMessage(`Opened ${TOP_LEVEL_LABELS[itemId]} menu.`);
					return;
				}

				if (itemId === 'quit') {
					exit();
					return;
				}

				setMessage(`${TOP_LEVEL_LABELS[itemId]} is not wired in the Ink prototype yet.`);
			}

			return;
		}

		if (screen === 'language') {
			if (key.upArrow) {
				setLanguageIndex(index => (index - 1 + uiModel.languages.length) % uiModel.languages.length);
				return;
			}

			if (key.downArrow) {
				setLanguageIndex(index => (index + 1) % uiModel.languages.length);
				return;
			}

			if (isEnter(input, key)) {
				setScreen('main');
				setMessage(`Language set to ${draft.languageLabel}.`);
			}

			return;
		}

		if (screen === 'color') {
			if (key.upArrow) {
				setColorIndex(index => (index - 1 + uiModel.colors.length) % uiModel.colors.length);
				return;
			}

			if (key.downArrow) {
				setColorIndex(index => (index + 1) % uiModel.colors.length);
				return;
			}

			if (isEnter(input, key)) {
				setScreen('main');
				setMessage(`Color draft set to ${draft.colorLabel || 'Default'}.`);
			}

			return;
		}

		if (screen === 'nickname') {
			if (isEnter(input, key)) {
				setSavedNickname(nicknameInput.trim());
				setNicknameInput('');
				setScreen('main');
				setMessage('Nickname draft saved.');
				return;
			}

			if (key.backspace || key.delete) {
				setNicknameInput(value => value.slice(0, -1));
				return;
			}

			if (!key.ctrl && !key.meta && input) {
				setNicknameInput(value => value + input);
			}
		}
	});

	const menuItems = uiModel.top_level_menu.map((itemId, index) => ({
		id: itemId,
		active: screen === 'main' && index === mainIndex,
		label: TOP_LEVEL_LABELS[itemId]
	}));

	const activeMenuId = screen === 'main' ? uiModel.top_level_menu[mainIndex] : screen;

	return inkBox(
		{flexDirection: 'column', paddingX: 1},
		inkBox(
			{marginBottom: 1},
			inkText({bold: true}, 'BuddyHub Ink DEV'),
			inkText({color: 'gray'}, '  Prototype UI on top of the current Python core')
		),
		inkBox(
			{gap: 2},
			inkBox(
				{flexDirection: 'column', borderStyle: 'round', borderColor: 'gray', paddingX: 1, width: 38},
				sectionTitle('Menu'),
				inkBox(
					{flexDirection: 'column', marginTop: 1},
					...menuItems.map(item => menuRow(item.id, item.active))
				),
				inkBox(
					{marginTop: 1, flexDirection: 'column'},
					sectionTitle('Selection'),
					inkText({color: 'gray'}, DETAILS[activeMenuId]),
					inkText({color: 'gray'}, `Current: ${topLevelValue(activeMenuId, draft)}`)
				),
				selectionPanel(screen, uiModel, languageIndex, colorIndex, nicknameInput)
			),
			previewCard(draft, currentVisual)
		),
		inkBox({marginTop: 1}, inkText({color: 'gray'}, message))
	);
}

function main() {
	if (process.argv.includes('--dump-prototype')) {
		const data = loadInitialData();
		process.stdout.write(JSON.stringify(data, null, 2));
		return;
	}

	const {state, ui} = loadInitialData();
	render(React.createElement(App, {initialState: state, uiModel: ui}));
}

main();
