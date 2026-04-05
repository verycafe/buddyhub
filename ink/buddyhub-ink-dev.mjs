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
const PYTHON_BRIDGE = path.join(ROOT, 'buddyhub_bridge.py');
let resolvedPythonCommand = null;

const TOP_LEVEL_LABELS = {
	language: 'Language',
	color: 'Color',
	nickname: 'Nickname',
	apply: 'Apply',
	restore: 'Restore',
	uninstall: 'Uninstall',
	quit: 'Quit'
};

const SETUP_LABELS = {
	binary: 'Claude binary path',
	config: 'Claude config path',
	retry: 'Retry detection',
	continue: 'Continue',
	quit: 'Quit'
};

const DETAILS = {
	setup: 'BuddyHub needs help locating Claude Code before the normal menu can open.',
	language: 'Choose the BuddyHub menu language.',
	color: 'Choose a Buddy color preset. Preview updates instantly.',
	nickname: 'Type a new Buddy display name and save it.',
	apply: 'Apply the current saved selection to Claude Code, then restart Claude Code.',
	restore: 'Restore the original official Buddy customization from backup.',
	uninstall: 'Restore official Buddy state, clear BuddyHub traces, then schedule automatic package uninstall.',
	quit: 'Exit the Ink development prototype.',
	setup_binary_input: 'Type the Claude executable path, then press Enter. Leave blank to clear.',
	setup_config_input: 'Type the Claude config path, then press Enter. Leave blank to clear.'
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

function resolvePythonCommand() {
	if (resolvedPythonCommand) {
		return resolvedPythonCommand;
	}

	const envPython = process.env.BUDDYHUB_PYTHON;
	const candidates = envPython
		? [{command: envPython, args: []}]
		: [
			{command: 'python3', args: []},
			{command: 'python', args: []},
			{command: 'py', args: ['-3']}
		];

	for (const candidate of candidates) {
		const probe = spawnSync(candidate.command, [...candidate.args, '--version'], {
			cwd: ROOT,
			encoding: 'utf8'
		});
		if (!probe.error && probe.status === 0) {
			resolvedPythonCommand = candidate;
			return candidate;
		}
	}

	throw new Error('BuddyHub requires Python 3. Set BUDDYHUB_PYTHON if Python is installed outside PATH.');
}

function runBridge(args) {
	const python = resolvePythonCommand();
	const result = spawnSync(python.command, [...python.args, PYTHON_BRIDGE, ...args], {
		cwd: ROOT,
		encoding: 'utf8'
	});

	if (result.error) {
		throw result.error;
	}

	if (result.status !== 0) {
		let parsed = null;
		try {
			parsed = JSON.parse(result.stdout || '{}');
		} catch {}
		if (parsed?.error) {
			throw new Error(parsed.error);
		}
		throw new Error((result.stderr || result.stdout || '').trim() || `${python.command} exited with ${result.status}`);
	}

	const payload = JSON.parse(result.stdout);
	if (payload && payload.ok === false) {
		throw new Error(payload.error || 'Bridge action failed');
	}
	return payload;
}

function loadInitialData() {
	const payload = runBridge(['dump-prototype']);
	return {state: payload.state, ui: payload.ui};
}

function topLevelValue(itemId, draft) {
	if (itemId === 'language') return draft.languageLabel;
	if (itemId === 'color') return draft.colorLabel || 'Default';
	if (itemId === 'nickname') return draft.nickname || draft.currentName || 'none';
	return '';
}

function menuRow(label, active, keyName = label) {
	return inkText(
		{key: keyName, color: active ? 'cyan' : undefined, bold: active},
		`${active ? '› ' : '  '}${label}`
	);
}

function optionRow(label, active, color, keyName = label) {
	return inkText(
		{key: keyName, color: active ? color || 'cyan' : color || undefined, bold: active},
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

function selectionPanel(screen, uiModel, stateData, languageIndex, colorIndex, nicknameInput, setupIndex, pathInput) {
	if (screen === 'language') {
		return inkBox(
			{marginTop: 1, flexDirection: 'column'},
			sectionTitle('Language Options'),
			...uiModel.languages.map((item, index) =>
				optionRow(item.label, index === languageIndex, index === languageIndex ? 'cyan' : undefined, item.language_id)
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
						color: item.available ? (index === colorIndex ? item.hex : undefined) : 'gray',
						bold: index === colorIndex
					},
					`${index === colorIndex ? '› ' : '  '}${item.label}  ${item.hex}${item.available ? '' : '  (unavailable)'}`
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

	if (screen === 'setup') {
		return inkBox(
			{marginTop: 1, flexDirection: 'column'},
			sectionTitle('Setup'),
			inkText({color: 'gray'}, stateData.setup?.intro || 'BuddyHub could not detect Claude Code automatically.'),
			inkBox({marginTop: 1, flexDirection: 'column'},
					...(uiModel.setup_menu || []).map((itemId, index) =>
					optionRow(SETUP_LABELS[itemId] || itemId, index === setupIndex, index === setupIndex ? 'cyan' : undefined, itemId)
				)
			)
		);
	}

	if (screen === 'setup_binary_input' || screen === 'setup_config_input') {
		const isBinary = screen === 'setup_binary_input';
		return inkBox(
			{marginTop: 1, flexDirection: 'column'},
			sectionTitle(isBinary ? 'Claude binary path' : 'Claude config path'),
			inkText({color: 'gray'}, DETAILS[screen]),
			inkText({}, `Input: ${pathInput || '|'}`)
		);
	}

	return null;
}

function setupCard(stateData) {
	const setup = stateData.setup || {};
	const binary = setup.binary || {};
	const config = setup.config || {};
	const renderLines = lines => (lines || []).slice(0, 4).map((line, index) => inkText({key: `${line}-${index}`, color: 'gray'}, line));
	return inkBox(
		{flexDirection: 'column', borderStyle: 'round', borderColor: 'yellow', paddingX: 1, width: 56},
		sectionTitle('Setup Guidance'),
		inkText({color: 'gray'}, setup.intro || 'BuddyHub could not fully detect Claude Code.'),
		inkBox({marginTop: 1, flexDirection: 'column'},
			inkText({bold: true}, 'Binary'),
			inkText({color: binary.detected ? 'green' : 'yellow'}, binary.detected ? 'Detected' : 'Missing'),
			binary.detected_path ? inkText({}, `Detected path: ${binary.detected_path}`) : null,
			binary.saved_path ? inkText({}, `Saved override: ${binary.saved_path}`) : null,
			binary.reason ? inkText({color: 'gray'}, `Reason: ${binary.reason}`) : null,
			...renderLines(binary.reference_lines),
		),
		inkBox({marginTop: 1, flexDirection: 'column'},
			inkText({bold: true}, 'Config'),
			inkText({color: config.detected ? 'green' : 'yellow'}, config.detected ? 'Detected' : 'Missing'),
			config.detected_path ? inkText({}, `Detected path: ${config.detected_path}`) : null,
			config.saved_path ? inkText({}, `Saved override: ${config.saved_path}`) : null,
			config.reason ? inkText({color: 'gray'}, `Reason: ${config.reason}`) : null,
			...renderLines(config.reference_lines),
		)
	);
}

function App({initialState, uiModel}) {
	const {exit} = useApp();
	const [stateData, setStateData] = useState(initialState);
	const [uiState, setUiState] = useState(uiModel);
	const [screen, setScreen] = useState(initialState.needs_setup ? 'setup' : 'main');
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
	const [setupIndex, setSetupIndex] = useState(0);
	const [nicknameInput, setNicknameInput] = useState('');
	const [savedNickname, setSavedNickname] = useState(initialState.settings.nickname || '');
	const [pathInput, setPathInput] = useState('');
	const [message, setMessage] = useState('Ink DEV prototype. Use arrows + Enter. Esc returns.');

	const currentVisual = stateData.current_visual || {};

	const syncFromSnapshot = ({state, ui}) => {
		const nextState = state || stateData;
		const nextUi = ui || uiState;
		if (ui) {
			setUiState(ui);
		}
		setStateData(nextState);
		const nextLanguage = nextState?.settings?.language_id || 'en';
		const nextLanguageIndex = nextUi.languages.findIndex(item => item.language_id === nextLanguage);
		setLanguageIndex(nextLanguageIndex >= 0 ? nextLanguageIndex : 0);
		const nextColor = nextState?.draft_visual?.color_id ?? nextState?.settings?.color_id ?? null;
		const nextColorIndex = nextUi.colors.findIndex(item => item.color_id === nextColor);
		setColorIndex(nextColorIndex >= 0 ? nextColorIndex : 0);
		setSavedNickname(nextState?.settings?.nickname || '');
	};

	const reloadPrototype = () => {
		const snapshot = loadInitialData();
		syncFromSnapshot(snapshot);
		return snapshot;
	};

	const performBridgeAction = (args, successMessage) => {
		try {
			const payload = runBridge(args);
			const snapshot = loadInitialData();
			syncFromSnapshot(snapshot);
			const nextState = snapshot.state;
			if (nextState?.needs_setup && !screen.startsWith('setup')) {
				setScreen('setup');
			}
			if (payload.result?.result_card?.detail) {
				setMessage(payload.result.result_card.detail);
				return;
			}
			setMessage(successMessage);
		} catch (error) {
			setMessage(`Action failed: ${error.message}`);
		}
	};

	const draft = useMemo(() => {
		const color = uiState.colors[colorIndex] || null;
		const language = uiState.languages[languageIndex] || uiState.languages[0];
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
	}, [colorIndex, currentVisual, languageIndex, nicknameInput, savedNickname, screen, uiState.colors, uiState.languages]);

	useInput((input, key) => {
		if (key.escape) {
			if (screen === 'main') {
				exit();
				return;
			}

			if (screen === 'nickname') {
				setNicknameInput('');
			}
			if (screen === 'setup_binary_input' || screen === 'setup_config_input') {
				setPathInput('');
				setScreen('setup');
				setMessage('Returned to Setup.');
				return;
			}
			if (screen === 'setup') {
				setMessage('Setup is still required before the normal menu can open.');
				return;
			}
			setScreen(stateData.needs_setup ? 'setup' : 'main');
			setMessage(stateData.needs_setup ? 'Returned to Setup.' : 'Returned to the main menu.');
			return;
		}

		if (input === 'q' && (screen === 'main' || screen === 'setup')) {
			exit();
			return;
		}

		if (screen === 'setup') {
			if (key.upArrow) {
				setSetupIndex(index => (index - 1 + uiState.setup_menu.length) % uiState.setup_menu.length);
				return;
			}

			if (key.downArrow) {
				setSetupIndex(index => (index + 1) % uiState.setup_menu.length);
				return;
			}

			if (isEnter(input, key)) {
				const itemId = uiState.setup_menu[setupIndex];
				if (itemId === 'binary') {
					setPathInput(stateData.setup?.binary?.saved_path || '');
					setScreen('setup_binary_input');
					setMessage('Editing Claude binary path.');
					return;
				}
				if (itemId === 'config') {
					setPathInput(stateData.setup?.config?.saved_path || '');
					setScreen('setup_config_input');
					setMessage('Editing Claude config path.');
					return;
				}
				if (itemId === 'retry') {
					const payload = runBridge(['retry-detection']);
					const snapshot = loadInitialData();
					syncFromSnapshot(snapshot);
					setScreen(snapshot.state.needs_setup ? 'setup' : 'main');
					setMessage(payload.state?.needs_setup ? (payload.state?.setup?.intro || 'Detection still needs setup.') : 'Detection succeeded. Opening main menu.');
					return;
				}
				if (itemId === 'continue') {
					setScreen('main');
					setMessage('Continuing with partial detection. Some actions may remain unavailable until Setup is complete.');
					return;
				}
				if (itemId === 'quit') {
					exit();
				}
			}

			return;
		}

		if (screen === 'setup_binary_input' || screen === 'setup_config_input') {
			if (isEnter(input, key)) {
				const trimmed = pathInput.trim();
				const args = screen === 'setup_binary_input'
					? (trimmed ? ['set-binary-path', trimmed] : ['set-binary-path'])
					: (trimmed ? ['set-config-path', trimmed] : ['set-config-path']);
				try {
					runBridge(args);
					const snapshot = loadInitialData();
					syncFromSnapshot(snapshot);
					setPathInput('');
					setScreen(snapshot.state.needs_setup ? 'setup' : 'main');
					setMessage(screen === 'setup_binary_input' ? 'Claude binary path saved.' : 'Claude config path saved.');
				} catch (error) {
					setMessage(`Action failed: ${error.message}`);
				}
				return;
			}

			if (key.backspace || key.delete) {
				setPathInput(value => value.slice(0, -1));
				return;
			}

			if (!key.ctrl && !key.meta && input) {
				setPathInput(value => value + input);
			}
			return;
		}

		if (screen === 'main') {
			if (key.upArrow) {
				setMainIndex(index => (index - 1 + uiState.top_level_menu.length) % uiState.top_level_menu.length);
				return;
			}

			if (key.downArrow) {
				setMainIndex(index => (index + 1) % uiState.top_level_menu.length);
				return;
			}

			if (isEnter(input, key)) {
				const itemId = uiState.top_level_menu[mainIndex];
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

				if (itemId === 'apply') {
					performBridgeAction(['apply'], 'Apply finished. Restart Claude Code to see the official Buddy update.');
					return;
				}

				if (itemId === 'restore') {
					performBridgeAction(['restore'], 'Restore finished.');
					return;
				}

				if (itemId === 'uninstall') {
					try {
						const payload = runBridge(['uninstall']);
						const notice = payload.state?.exit_notice || payload.result?.result_card?.detail || 'BuddyHub cleanup has been scheduled.';
						process.stdout.write(`${notice}\n`);
						exit();
					} catch (error) {
						setMessage(`Action failed: ${error.message}`);
					}
					return;
				}

				setMessage(`${TOP_LEVEL_LABELS[itemId]} is not wired in the Ink prototype yet.`);
			}

			return;
		}

		if (screen === 'language') {
			if (key.upArrow) {
				setLanguageIndex(index => (index - 1 + uiState.languages.length) % uiState.languages.length);
				return;
			}

			if (key.downArrow) {
				setLanguageIndex(index => (index + 1) % uiState.languages.length);
				return;
			}

			if (isEnter(input, key)) {
				const selected = uiState.languages[languageIndex];
				performBridgeAction(['set-language', selected.language_id], `Language set to ${selected.label}.`);
				setScreen('main');
			}

			return;
		}

		if (screen === 'color') {
			if (key.upArrow) {
				setColorIndex(index => (index - 1 + uiState.colors.length) % uiState.colors.length);
				return;
			}

			if (key.downArrow) {
				setColorIndex(index => (index + 1) % uiState.colors.length);
				return;
			}

			if (isEnter(input, key)) {
				const selected = uiState.colors[colorIndex];
				if (!selected.available) {
					setMessage(`Action failed: ${selected.reason || 'Selected color is unavailable.'}`);
					return;
				}
				performBridgeAction(['set-color', selected.color_id], `Color saved as ${selected.label}.`);
				setScreen(stateData.needs_setup ? 'setup' : 'main');
			}

			return;
		}

		if (screen === 'nickname') {
			if (isEnter(input, key)) {
				const nextNickname = nicknameInput.trim();
				if (nextNickname) {
					performBridgeAction(['set-nickname', nextNickname], 'Nickname saved.');
				} else {
					performBridgeAction(['clear-nickname'], 'Nickname cleared.');
				}
				setNicknameInput('');
				setScreen(stateData.needs_setup ? 'setup' : 'main');
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

	const menuItems = uiState.top_level_menu.map((itemId, index) => ({
		id: itemId,
		active: screen === 'main' && index === mainIndex,
		label: TOP_LEVEL_LABELS[itemId]
	}));

	const activeMenuId = screen === 'main'
		? uiState.top_level_menu[mainIndex]
		: (screen === 'setup' ? 'setup' : screen);

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
				sectionTitle(screen.startsWith('setup') ? 'Setup' : 'Menu'),
				inkBox(
					{flexDirection: 'column', marginTop: 1},
					...(screen === 'setup'
						? (uiState.setup_menu || []).map((itemId, index) => menuRow(SETUP_LABELS[itemId] || itemId, index === setupIndex, itemId))
						: menuItems.map(item => menuRow(item.label, item.active, item.id)))
				),
				inkBox(
					{marginTop: 1, flexDirection: 'column'},
					sectionTitle('Selection'),
					inkText({color: 'gray'}, DETAILS[activeMenuId]),
					(activeMenuId === 'language' || activeMenuId === 'color' || activeMenuId === 'nickname')
						? inkText({color: 'gray'}, `Current: ${topLevelValue(activeMenuId, draft)}`)
						: null
				),
				selectionPanel(screen, uiState, stateData, languageIndex, colorIndex, nicknameInput, setupIndex, pathInput)
			),
			(screen.startsWith('setup') ? setupCard(stateData) : previewCard(draft, currentVisual))
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
