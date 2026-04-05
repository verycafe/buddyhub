#!/usr/bin/env python3
from __future__ import annotations

import argparse
import curses
import json
import locale
from typing import Any

from plugins.buddyhub.scripts.buddyhublib import (
    COLOR_PRESETS,
    LANGUAGE_PRESETS,
    apply_installed_patch,
    inspect_native_patch,
    load_customization_settings,
    preview_lines_for_customization,
    restore_native_patch,
    update_customization_settings,
)

locale.setlocale(locale.LC_ALL, "")

LANGUAGE_PACKS: dict[str, dict[str, str]] = {
    "en": {
        "title": "BuddyHub",
        "subtitle": "Official Buddy configurator",
        "menu_language": "Language",
        "menu_color": "Color",
        "menu_nickname": "Nickname",
        "menu_apply": "Apply",
        "menu_restore": "Restore",
        "menu_quit": "Quit",
        "screen_language": "Language Menu",
        "screen_color": "Color Menu",
        "screen_nickname": "Nickname Input",
        "preview": "Preview",
        "buddy_identity": "Buddy",
        "display_name": "Display name",
        "selected_language": "Language",
        "selected_color": "Color",
        "selected_nickname": "Nickname",
        "installed_element": "Installed element",
        "apply_ready": "Apply ready",
        "value_none": "none",
        "value_unknown": "unknown",
        "help_main": "Up/Down: move  Enter: select  q: quit",
        "help_submenu": "Up/Down: move  Enter: select  Esc/q: back",
        "help_input": "Type nickname. Enter: save  Esc: cancel  Backspace: delete",
        "help_result": "Enter/Esc/q: return to menu",
        "nickname_prompt": "Enter nickname (leave blank to clear):",
        "nickname_current": "Current display name",
        "nickname_draft": "Draft nickname",
        "nickname_input": "Input",
        "saved_language": "Language saved.",
        "saved_color": "Color saved.",
        "saved_nickname": "Nickname saved.",
        "cleared_nickname": "Nickname cleared.",
        "apply_success": "Applied. Restart Claude Code to reload the official Buddy.",
        "restore_success": "Restored original Buddy customization.",
        "action_failed": "Action failed",
        "unavailable": "unavailable",
        "current": "current",
        "pending": "pending",
        "default_color": "Default",
        "clear_color_saved": "Color cleared.",
        "restart_note": "Apply changes require a Claude Code restart.",
        "menu_header": "Menu",
        "status_header": "Status",
        "summary_header": "Summary",
        "installed_state": "Installed State",
        "draft_state": "Draft State",
        "installed_preview": "Installed Preview",
        "draft_preview": "Draft Preview",
        "draft": "draft",
        "available": "available",
        "color_menu_hint": "Pick a color. Enter saves the draft. Apply from the main menu.",
        "changes_label": "Changes",
        "changes_none": "none",
        "change_color": "color",
        "change_nickname": "nickname",
        "menu_state_clean": "up to date",
        "menu_state_pending": "pending",
        "menu_state_restore_ready": "available",
        "menu_state_restore_empty": "none",
        "status_pending_changes": "Pending changes",
        "status_restore": "Restore",
        "status_yes": "yes",
        "status_no": "no",
        "message_no_pending_changes": "No pending changes to apply.",
        "message_no_restore": "Nothing to restore.",
        "detail_header": "Selection",
        "detail_language": "Switch the UI language for the BuddyHub configurator.",
        "detail_color": "Choose the Buddy color. The draft preview updates immediately.",
        "detail_nickname": "Set the displayed Buddy name. The draft preview updates while you type.",
        "detail_apply": "Write the current draft to Claude Code. Restart Claude Code after applying.",
        "detail_restore": "Restore the original official Buddy customization from backup.",
        "detail_quit": "Exit BuddyHub without applying new changes.",
        "detail_color_status": "Availability",
        "detail_color_reason": "Reason",
        "detail_language_hint": "The menu language changes immediately after selection.",
        "detail_nickname_hint": "Press Enter to save the nickname draft, then Apply from the main menu.",
        "result_apply_title": "Apply Result",
        "result_restore_title": "Restore Result",
        "result_error_title": "Action Result",
        "result_status": "Status",
        "result_next_step": "Next step",
        "result_restart_needed": "Restart Claude Code to reload the official Buddy.",
        "result_restore_ready": "The original Buddy state has been restored.",
        "result_return_hint": "Press Enter, Esc, or q to return to the main menu.",
    },
    "zh_cn": {
        "title": "BuddyHub",
        "subtitle": "官方 Buddy 配置器",
        "menu_language": "语言",
        "menu_color": "颜色",
        "menu_nickname": "昵称",
        "menu_apply": "应用",
        "menu_restore": "恢复",
        "menu_quit": "退出",
        "screen_language": "语言菜单",
        "screen_color": "颜色菜单",
        "screen_nickname": "昵称输入",
        "preview": "预览",
        "buddy_identity": "Buddy",
        "display_name": "显示名称",
        "selected_language": "语言",
        "selected_color": "颜色",
        "selected_nickname": "昵称",
        "installed_element": "当前元素",
        "apply_ready": "可应用",
        "value_none": "无",
        "value_unknown": "未知",
        "help_main": "上下键：移动  回车：选择  q：退出",
        "help_submenu": "上下键：移动  回车：选择  Esc/q：返回",
        "help_input": "输入昵称。回车：保存  Esc：取消  退格：删除",
        "help_result": "回车/Esc/q：返回菜单",
        "nickname_prompt": "输入昵称（留空则清除）：",
        "nickname_current": "当前显示名",
        "nickname_draft": "草稿昵称",
        "nickname_input": "输入框",
        "saved_language": "语言已保存。",
        "saved_color": "颜色已保存。",
        "saved_nickname": "昵称已保存。",
        "cleared_nickname": "昵称已清除。",
        "apply_success": "已应用。请重启 Claude Code 以重新加载官方 Buddy。",
        "restore_success": "已恢复原始 Buddy 配置。",
        "action_failed": "操作失败",
        "unavailable": "不可用",
        "current": "当前",
        "pending": "待定",
        "default_color": "默认",
        "clear_color_saved": "颜色已清除。",
        "restart_note": "应用后需要重启 Claude Code。",
        "menu_header": "菜单",
        "status_header": "状态",
        "summary_header": "摘要",
        "installed_state": "已安装状态",
        "draft_state": "草稿状态",
        "installed_preview": "已安装预览",
        "draft_preview": "草稿预览",
        "draft": "草稿",
        "available": "可用",
        "color_menu_hint": "选择颜色。回车保存到草稿，再回主菜单应用。",
        "changes_label": "变化",
        "changes_none": "无",
        "change_color": "颜色",
        "change_nickname": "昵称",
        "menu_state_clean": "已同步",
        "menu_state_pending": "待应用",
        "menu_state_restore_ready": "可恢复",
        "menu_state_restore_empty": "无",
        "status_pending_changes": "待应用变更",
        "status_restore": "恢复能力",
        "status_yes": "是",
        "status_no": "否",
        "message_no_pending_changes": "当前没有需要应用的变更。",
        "message_no_restore": "当前没有可恢复的内容。",
        "detail_header": "当前选择",
        "detail_language": "切换 BuddyHub 配置器的界面语言。",
        "detail_color": "选择 Buddy 颜色。草稿预览会立即更新。",
        "detail_nickname": "设置 Buddy 显示名称。输入时草稿预览会立即更新。",
        "detail_apply": "把当前草稿写入 Claude Code。应用后需要重启 Claude Code。",
        "detail_restore": "从备份恢复原始官方 Buddy 配置。",
        "detail_quit": "退出 BuddyHub，不应用新的更改。",
        "detail_color_status": "可用性",
        "detail_color_reason": "原因",
        "detail_language_hint": "选择后菜单语言会立刻切换。",
        "detail_nickname_hint": "回车保存昵称草稿，然后回主菜单应用。",
        "result_apply_title": "应用结果",
        "result_restore_title": "恢复结果",
        "result_error_title": "操作结果",
        "result_status": "状态",
        "result_next_step": "下一步",
        "result_restart_needed": "请重启 Claude Code 以重新加载官方 Buddy。",
        "result_restore_ready": "原始 Buddy 状态已恢复。",
        "result_return_hint": "按回车、Esc 或 q 返回主菜单。",
    },
    "zh_hans": {},
    "ja": {
        "title": "BuddyHub",
        "subtitle": "公式 Buddy 設定ツール",
        "menu_language": "言語",
        "menu_color": "色",
        "menu_nickname": "ニックネーム",
        "menu_apply": "適用",
        "menu_restore": "復元",
        "menu_quit": "終了",
        "screen_language": "言語メニュー",
        "screen_color": "カラーメニュー",
        "screen_nickname": "ニックネーム入力",
        "preview": "プレビュー",
        "buddy_identity": "Buddy",
        "display_name": "表示名",
        "selected_language": "言語",
        "selected_color": "色",
        "selected_nickname": "ニックネーム",
        "installed_element": "現在の要素",
        "apply_ready": "適用可能",
        "value_none": "なし",
        "value_unknown": "不明",
        "help_main": "上下: 移動  Enter: 選択  q: 終了",
        "help_submenu": "上下: 移動  Enter: 選択  Esc/q: 戻る",
        "help_input": "ニックネーム入力。Enter: 保存  Esc: 取消  Backspace: 削除",
        "help_result": "Enter/Esc/q: メニューへ戻る",
        "nickname_prompt": "ニックネームを入力（空でクリア）:",
        "nickname_current": "現在の表示名",
        "nickname_draft": "下書きニックネーム",
        "nickname_input": "入力欄",
        "saved_language": "言語を保存しました。",
        "saved_color": "色を保存しました。",
        "saved_nickname": "ニックネームを保存しました。",
        "cleared_nickname": "ニックネームを消去しました。",
        "apply_success": "適用しました。Claude Code を再起動してください。",
        "restore_success": "Buddy 設定を復元しました。",
        "action_failed": "操作に失敗しました",
        "unavailable": "未対応",
        "current": "現在",
        "pending": "保留",
        "default_color": "デフォルト",
        "clear_color_saved": "色をクリアしました。",
        "restart_note": "適用後は Claude Code の再起動が必要です。",
        "menu_header": "メニュー",
        "status_header": "状態",
        "summary_header": "概要",
        "installed_state": "適用中の状態",
        "draft_state": "下書き状態",
        "installed_preview": "適用中プレビュー",
        "draft_preview": "下書きプレビュー",
        "draft": "下書き",
        "available": "利用可",
        "color_menu_hint": "色を選択。Enter で下書き保存、メインメニューで適用。",
        "changes_label": "変更点",
        "changes_none": "なし",
        "change_color": "色",
        "change_nickname": "ニックネーム",
        "menu_state_clean": "最新",
        "menu_state_pending": "未適用",
        "menu_state_restore_ready": "利用可",
        "menu_state_restore_empty": "なし",
        "status_pending_changes": "未適用の変更",
        "status_restore": "復元",
        "status_yes": "はい",
        "status_no": "いいえ",
        "message_no_pending_changes": "適用する変更はありません。",
        "message_no_restore": "復元する内容がありません。",
        "detail_header": "選択中",
        "detail_language": "BuddyHub 設定ツールの表示言語を切り替えます。",
        "detail_color": "Buddy の色を選びます。下書きプレビューはすぐ更新されます。",
        "detail_nickname": "Buddy の表示名を設定します。入力中に下書きプレビューが更新されます。",
        "detail_apply": "現在の下書きを Claude Code に書き込みます。適用後は再起動が必要です。",
        "detail_restore": "バックアップから公式 Buddy 設定を復元します。",
        "detail_quit": "BuddyHub を終了し、新しい変更は適用しません。",
        "detail_color_status": "利用可否",
        "detail_color_reason": "理由",
        "detail_language_hint": "選択後すぐにメニュー言語が切り替わります。",
        "detail_nickname_hint": "Enter でニックネーム下書きを保存し、メインメニューで適用します。",
        "result_apply_title": "適用結果",
        "result_restore_title": "復元結果",
        "result_error_title": "操作結果",
        "result_status": "状態",
        "result_next_step": "次の手順",
        "result_restart_needed": "Claude Code を再起動して公式 Buddy を再読込してください。",
        "result_restore_ready": "元の Buddy 状態を復元しました。",
        "result_return_hint": "Enter、Esc、q でメインメニューに戻ります。",
    },
    "de": {
        "title": "BuddyHub",
        "subtitle": "Offizieller Buddy-Konfigurator",
        "menu_language": "Sprache",
        "menu_color": "Farbe",
        "menu_nickname": "Spitzname",
        "menu_apply": "Anwenden",
        "menu_restore": "Wiederherstellen",
        "menu_quit": "Beenden",
        "screen_language": "Sprachmenü",
        "screen_color": "Farbmenü",
        "screen_nickname": "Spitzname eingeben",
        "preview": "Vorschau",
        "buddy_identity": "Buddy",
        "display_name": "Anzeigename",
        "selected_language": "Sprache",
        "selected_color": "Farbe",
        "selected_nickname": "Spitzname",
        "installed_element": "Installiertes Element",
        "apply_ready": "Anwendbar",
        "value_none": "keins",
        "value_unknown": "unbekannt",
        "help_main": "Hoch/Runter: bewegen  Enter: wählen  q: beenden",
        "help_submenu": "Hoch/Runter: bewegen  Enter: wählen  Esc/q: zurück",
        "help_input": "Spitzname eingeben. Enter: speichern  Esc: abbrechen  Backspace: löschen",
        "help_result": "Enter/Esc/q: zurück zum Menü",
        "nickname_prompt": "Spitznamen eingeben (leer = löschen):",
        "nickname_current": "Aktueller Anzeigename",
        "nickname_draft": "Entwurfs-Spitzname",
        "nickname_input": "Eingabe",
        "saved_language": "Sprache gespeichert.",
        "saved_color": "Farbe gespeichert.",
        "saved_nickname": "Spitzname gespeichert.",
        "cleared_nickname": "Spitzname gelöscht.",
        "apply_success": "Angewendet. Claude Code neu starten.",
        "restore_success": "Originale Buddy-Anpassung wiederhergestellt.",
        "action_failed": "Aktion fehlgeschlagen",
        "unavailable": "nicht verfügbar",
        "current": "aktuell",
        "pending": "ausstehend",
        "default_color": "Standard",
        "clear_color_saved": "Farbe gelöscht.",
        "restart_note": "Nach dem Anwenden ist ein Neustart von Claude Code nötig.",
        "menu_header": "Menü",
        "status_header": "Status",
        "summary_header": "Übersicht",
        "installed_state": "Installierter Zustand",
        "draft_state": "Entwurfszustand",
        "installed_preview": "Installierte Vorschau",
        "draft_preview": "Entwurfsvorschau",
        "draft": "Entwurf",
        "available": "verfügbar",
        "color_menu_hint": "Farbe wählen. Enter speichert den Entwurf, Anwenden im Hauptmenü.",
        "changes_label": "Änderungen",
        "changes_none": "keine",
        "change_color": "Farbe",
        "change_nickname": "Spitzname",
        "menu_state_clean": "aktuell",
        "menu_state_pending": "ausstehend",
        "menu_state_restore_ready": "verfügbar",
        "menu_state_restore_empty": "keine",
        "status_pending_changes": "Ausstehende Änderungen",
        "status_restore": "Wiederherstellung",
        "status_yes": "ja",
        "status_no": "nein",
        "message_no_pending_changes": "Es gibt keine Änderungen zum Anwenden.",
        "message_no_restore": "Es gibt nichts wiederherzustellen.",
        "detail_header": "Auswahl",
        "detail_language": "Wechselt die Sprache der BuddyHub-Oberfläche.",
        "detail_color": "Wählt die Buddy-Farbe. Die Entwurfsvorschau aktualisiert sich sofort.",
        "detail_nickname": "Setzt den angezeigten Buddy-Namen. Die Entwurfsvorschau reagiert beim Tippen.",
        "detail_apply": "Schreibt den aktuellen Entwurf in Claude Code. Danach Claude Code neu starten.",
        "detail_restore": "Stellt die ursprüngliche offizielle Buddy-Anpassung aus dem Backup wieder her.",
        "detail_quit": "Beendet BuddyHub ohne neue Änderungen anzuwenden.",
        "detail_color_status": "Verfügbarkeit",
        "detail_color_reason": "Grund",
        "detail_language_hint": "Die Menüsprache wechselt sofort nach der Auswahl.",
        "detail_nickname_hint": "Mit Enter den Spitznamen-Entwurf speichern und dann im Hauptmenü anwenden.",
        "result_apply_title": "Anwendungsergebnis",
        "result_restore_title": "Wiederherstellung",
        "result_error_title": "Aktionsergebnis",
        "result_status": "Status",
        "result_next_step": "Nächster Schritt",
        "result_restart_needed": "Claude Code neu starten, um den offiziellen Buddy neu zu laden.",
        "result_restore_ready": "Der ursprüngliche Buddy-Zustand wurde wiederhergestellt.",
        "result_return_hint": "Enter, Esc oder q kehren zum Hauptmenü zurück.",
    },
    "fr": {
        "title": "BuddyHub",
        "subtitle": "Configurateur du Buddy officiel",
        "menu_language": "Langue",
        "menu_color": "Couleur",
        "menu_nickname": "Surnom",
        "menu_apply": "Appliquer",
        "menu_restore": "Restaurer",
        "menu_quit": "Quitter",
        "screen_language": "Menu Langue",
        "screen_color": "Menu Couleur",
        "screen_nickname": "Saisie du surnom",
        "preview": "Aperçu",
        "buddy_identity": "Buddy",
        "display_name": "Nom affiché",
        "selected_language": "Langue",
        "selected_color": "Couleur",
        "selected_nickname": "Surnom",
        "installed_element": "Élément installé",
        "apply_ready": "Application prête",
        "value_none": "aucun",
        "value_unknown": "inconnu",
        "help_main": "Haut/Bas: déplacer  Entrée: choisir  q: quitter",
        "help_submenu": "Haut/Bas: déplacer  Entrée: choisir  Esc/q: retour",
        "help_input": "Saisir le surnom. Entrée: enregistrer  Esc: annuler  Retour arrière: supprimer",
        "help_result": "Entrée/Esc/q : retour au menu",
        "nickname_prompt": "Entrer le surnom (vide pour effacer) :",
        "nickname_current": "Nom affiché actuel",
        "nickname_draft": "Surnom brouillon",
        "nickname_input": "Saisie",
        "saved_language": "Langue enregistrée.",
        "saved_color": "Couleur enregistrée.",
        "saved_nickname": "Surnom enregistré.",
        "cleared_nickname": "Surnom effacé.",
        "apply_success": "Appliqué. Redémarrez Claude Code.",
        "restore_success": "Personnalisation Buddy restaurée.",
        "action_failed": "Échec de l'action",
        "unavailable": "indisponible",
        "current": "actuel",
        "pending": "en attente",
        "default_color": "Par défaut",
        "clear_color_saved": "Couleur effacée.",
        "restart_note": "Un redémarrage de Claude Code est nécessaire après application.",
        "menu_header": "Menu",
        "status_header": "Statut",
        "summary_header": "Résumé",
        "installed_state": "État installé",
        "draft_state": "État brouillon",
        "installed_preview": "Aperçu installé",
        "draft_preview": "Aperçu brouillon",
        "draft": "brouillon",
        "available": "disponible",
        "color_menu_hint": "Choisissez une couleur. Entrée enregistre le brouillon, appliquez depuis le menu principal.",
        "changes_label": "Changements",
        "changes_none": "aucun",
        "change_color": "couleur",
        "change_nickname": "surnom",
        "menu_state_clean": "à jour",
        "menu_state_pending": "en attente",
        "menu_state_restore_ready": "disponible",
        "menu_state_restore_empty": "aucun",
        "status_pending_changes": "Changements en attente",
        "status_restore": "Restauration",
        "status_yes": "oui",
        "status_no": "non",
        "message_no_pending_changes": "Aucun changement à appliquer.",
        "message_no_restore": "Rien à restaurer.",
        "detail_header": "Sélection",
        "detail_language": "Change la langue de l'interface BuddyHub.",
        "detail_color": "Choisit la couleur du Buddy. Le brouillon se met à jour immédiatement.",
        "detail_nickname": "Définit le nom affiché du Buddy. Le brouillon réagit pendant la saisie.",
        "detail_apply": "Écrit le brouillon actuel dans Claude Code. Redémarrez ensuite Claude Code.",
        "detail_restore": "Restaure la personnalisation officielle du Buddy depuis la sauvegarde.",
        "detail_quit": "Quitte BuddyHub sans appliquer de nouvelles modifications.",
        "detail_color_status": "Disponibilité",
        "detail_color_reason": "Raison",
        "detail_language_hint": "La langue du menu change immédiatement après la sélection.",
        "detail_nickname_hint": "Appuyez sur Entrée pour enregistrer le surnom brouillon, puis appliquez-le depuis le menu principal.",
        "result_apply_title": "Résultat de l'application",
        "result_restore_title": "Résultat de la restauration",
        "result_error_title": "Résultat de l'action",
        "result_status": "Statut",
        "result_next_step": "Étape suivante",
        "result_restart_needed": "Redémarrez Claude Code pour recharger le Buddy officiel.",
        "result_restore_ready": "L'état Buddy d'origine a été restauré.",
        "result_return_hint": "Appuyez sur Entrée, Esc ou q pour revenir au menu principal.",
    },
    "ru": {
        "title": "BuddyHub",
        "subtitle": "Настройка официального Buddy",
        "menu_language": "Язык",
        "menu_color": "Цвет",
        "menu_nickname": "Ник",
        "menu_apply": "Применить",
        "menu_restore": "Восстановить",
        "menu_quit": "Выход",
        "screen_language": "Меню языка",
        "screen_color": "Меню цвета",
        "screen_nickname": "Ввод ника",
        "preview": "Предпросмотр",
        "buddy_identity": "Buddy",
        "display_name": "Отображаемое имя",
        "selected_language": "Язык",
        "selected_color": "Цвет",
        "selected_nickname": "Ник",
        "installed_element": "Текущий элемент",
        "apply_ready": "Готово к применению",
        "value_none": "нет",
        "value_unknown": "неизвестно",
        "help_main": "Вверх/Вниз: выбор  Enter: открыть  q: выход",
        "help_submenu": "Вверх/Вниз: выбор  Enter: применить  Esc/q: назад",
        "help_input": "Введите ник. Enter: сохранить  Esc: отмена  Backspace: удалить",
        "help_result": "Enter/Esc/q: вернуться в меню",
        "nickname_prompt": "Введите ник (пусто = очистить):",
        "nickname_current": "Текущее отображаемое имя",
        "nickname_draft": "Ник в черновике",
        "nickname_input": "Ввод",
        "saved_language": "Язык сохранён.",
        "saved_color": "Цвет сохранён.",
        "saved_nickname": "Ник сохранён.",
        "cleared_nickname": "Ник очищен.",
        "apply_success": "Применено. Перезапустите Claude Code.",
        "restore_success": "Настройки Buddy восстановлены.",
        "action_failed": "Ошибка действия",
        "unavailable": "недоступно",
        "current": "текущий",
        "pending": "ожидает",
        "default_color": "По умолчанию",
        "clear_color_saved": "Цвет очищен.",
        "restart_note": "После применения нужно перезапустить Claude Code.",
        "menu_header": "Меню",
        "status_header": "Статус",
        "summary_header": "Сводка",
        "installed_state": "Текущее состояние",
        "draft_state": "Черновик",
        "installed_preview": "Текущий предпросмотр",
        "draft_preview": "Предпросмотр черновика",
        "draft": "черновик",
        "available": "доступно",
        "color_menu_hint": "Выберите цвет. Enter сохранит черновик, затем примените из главного меню.",
        "changes_label": "Изменения",
        "changes_none": "нет",
        "change_color": "цвет",
        "change_nickname": "ник",
        "menu_state_clean": "актуально",
        "menu_state_pending": "ожидает",
        "menu_state_restore_ready": "доступно",
        "menu_state_restore_empty": "нет",
        "status_pending_changes": "Ожидающие изменения",
        "status_restore": "Восстановление",
        "status_yes": "да",
        "status_no": "нет",
        "message_no_pending_changes": "Нет изменений для применения.",
        "message_no_restore": "Нечего восстанавливать.",
        "detail_header": "Выбор",
        "detail_language": "Переключает язык интерфейса BuddyHub.",
        "detail_color": "Выбирает цвет Buddy. Черновой предпросмотр обновляется сразу.",
        "detail_nickname": "Задаёт отображаемое имя Buddy. Предпросмотр меняется во время ввода.",
        "detail_apply": "Записывает текущий черновик в Claude Code. После этого перезапустите Claude Code.",
        "detail_restore": "Восстанавливает исходную официальную настройку Buddy из резервной копии.",
        "detail_quit": "Выходит из BuddyHub без применения новых изменений.",
        "detail_color_status": "Доступность",
        "detail_color_reason": "Причина",
        "detail_language_hint": "Язык меню переключается сразу после выбора.",
        "detail_nickname_hint": "Нажмите Enter, чтобы сохранить черновик ника, затем примените его из главного меню.",
        "result_apply_title": "Результат применения",
        "result_restore_title": "Результат восстановления",
        "result_error_title": "Результат действия",
        "result_status": "Статус",
        "result_next_step": "Следующий шаг",
        "result_restart_needed": "Перезапустите Claude Code, чтобы перезагрузить официальный Buddy.",
        "result_restore_ready": "Исходное состояние Buddy восстановлено.",
        "result_return_hint": "Нажмите Enter, Esc или q, чтобы вернуться в главное меню.",
    },
}

LANGUAGE_PACKS["zh_hans"] = dict(LANGUAGE_PACKS["zh_cn"])

LANGUAGE_ORDER = ["zh_cn", "en", "ja", "zh_hans", "de", "fr", "ru"]
TOP_LEVEL_MENU = ["language", "color", "nickname", "apply", "restore", "quit"]
VISIBLE_ELEMENT_CONTROLS = False


class BuddyHubTUI:
    def __init__(self) -> None:
        self.screen = "main"
        self.selection = {
            "main": 0,
            "language": 0,
            "color": 0,
        }
        self.message = ""
        self.result_card: dict[str, Any] | None = None
        self.nickname_buffer = ""
        self.running = True
        self.settings = load_customization_settings()
        self.lang = str(self.settings.get("language_id") or "en")
        self.inspection = inspect_native_patch()
        self.current_visual = self.inspection.get("current_visual") or {}
        self.sync_hidden_element_setting()
        self.draft_visual = self.build_draft_visual()
        self.color_pairs_ready = False

    def strings(self) -> dict[str, str]:
        return LANGUAGE_PACKS.get(self.lang, LANGUAGE_PACKS["en"])

    def tr(self, key: str) -> str:
        return self.strings().get(key, key)

    def refresh(self) -> None:
        self.settings = load_customization_settings()
        self.lang = str(self.settings.get("language_id") or "en")
        self.inspection = inspect_native_patch()
        self.current_visual = self.inspection.get("current_visual") or {}
        self.sync_hidden_element_setting()
        self.draft_visual = self.build_draft_visual()

    def build_draft_visual(self) -> dict[str, Any]:
        customization = self.inspection.get("customization") or {}
        effective_settings = self.inspection.get("effective_settings") or self.settings
        companion = self.inspection.get("companion_config") or {}
        if VISIBLE_ELEMENT_CONTROLS:
            preview_lines = preview_lines_for_customization(customization) or self.current_visual.get("preview_lines")
            element_id = effective_settings.get("element_id")
        else:
            preview_lines = self.current_visual.get("preview_lines")
            element_id = self.current_visual.get("element_id") or effective_settings.get("element_id")
        return {
            "name": effective_settings.get("nickname") or companion.get("name") or self.current_visual.get("name"),
            "species": self.current_visual.get("species"),
            "element_id": element_id,
            "color_id": effective_settings.get("color_id") or self.current_visual.get("color_id"),
            "preview_lines": preview_lines,
        }

    def sync_hidden_element_setting(self) -> None:
        if VISIBLE_ELEMENT_CONTROLS:
            return
        installed_element = self.current_visual.get("element_id")
        if installed_element is None:
            if self.settings.get("element_id") is None:
                return
            update_customization_settings(clear_element=True)
            self.refresh()
            return
        if self.settings.get("element_id") == installed_element:
            return
        update_customization_settings(element_id=installed_element)
        self.refresh()

    def current_language_index(self) -> int:
        current = self.settings.get("language_id") or "en"
        try:
            return LANGUAGE_ORDER.index(current)
        except ValueError:
            return 0

    def current_color_index(self) -> int:
        current = self.settings.get("color_id")
        entries = self.color_menu_entries()
        for index, entry in enumerate(entries):
            if entry["color_id"] == current:
                return index
        return 0

    def color_ids(self) -> list[str]:
        ordered = ["green", "orange", "blue", "pink", "purple", "red", "black", "white"]
        return [color_id for color_id in ordered if color_id in COLOR_PRESETS]

    def color_menu_entries(self) -> list[dict[str, Any]]:
        color_options = {
            item["color_id"]: item
            for item in self.inspection["customization"]["color_options"]
        }
        entries: list[dict[str, Any]] = [
            {
                "color_id": None,
                "label": self.tr("default_color"),
                "available": True,
            }
        ]
        for color_id in self.color_ids():
            option = color_options.get(color_id, {})
            entries.append(
                {
                    "color_id": color_id,
                    "label": self.color_option_label(color_id),
                    "available": bool(option.get("available", False)),
                }
            )
        return entries

    def top_level_label(self, item_id: str) -> str:
        return {
            "language": self.tr("menu_language"),
            "color": self.tr("menu_color"),
            "nickname": self.tr("menu_nickname"),
            "apply": self.tr("menu_apply"),
            "restore": self.tr("menu_restore"),
            "quit": self.tr("menu_quit"),
        }[item_id]

    def language_option_label(self, language_id: str) -> str:
        return LANGUAGE_PRESETS[language_id]["label"]

    def color_option_label(self, color_id: str) -> str:
        return COLOR_PRESETS[color_id]["label"]

    def color_chip(self, color_id: str | None) -> str:
        if color_id is None:
            return "[----]"
        if color_id == "white":
            return "[++++]"
        if color_id == "black":
            return "[####]"
        return "[####]"

    def set_message(self, message: str) -> None:
        self.message = message

    def preview_color_override(self) -> str | None:
        if self.screen != "color":
            return None
        entries = self.color_menu_entries()
        index = self.selection.get("color", 0)
        if 0 <= index < len(entries):
            return entries[index]["color_id"]
        return None

    def preview_nickname_override(self) -> str | None:
        if self.screen != "nickname":
            return None
        return self.nickname_buffer

    def preview_draft_visual(self) -> dict[str, Any]:
        visual = dict(self.draft_visual)
        preview_color = self.preview_color_override()
        preview_nickname = self.preview_nickname_override()
        if self.screen == "color":
            visual["color_id"] = preview_color or self.current_visual.get("color_id")
        if self.screen == "nickname":
            visual["name"] = preview_nickname or self.current_visual.get("name")
        return visual

    def draft_change_labels(self, visual: dict[str, Any] | None = None) -> list[str]:
        visual = visual or self.draft_visual
        changes: list[str] = []
        if visual.get("color_id") != self.current_visual.get("color_id"):
            changes.append(self.tr("change_color"))
        if visual.get("name") != self.current_visual.get("name"):
            changes.append(self.tr("change_nickname"))
        return changes

    def has_pending_changes(self, visual: dict[str, Any] | None = None) -> bool:
        return bool(self.draft_change_labels(visual))

    def color_changed(self, visual: dict[str, Any] | None = None) -> bool:
        visual = visual or self.draft_visual
        return visual.get("color_id") != self.current_visual.get("color_id")

    def nickname_changed(self, visual: dict[str, Any] | None = None) -> bool:
        visual = visual or self.draft_visual
        return visual.get("name") != self.current_visual.get("name")

    def has_restore_target(self) -> bool:
        patch_state = self.inspection.get("patch_state") or {}
        return bool(patch_state.get("installed"))

    def main_menu_value(self, item_id: str) -> str:
        if item_id == "language":
            return self.language_option_label(str(self.settings.get("language_id") or "en"))
        if item_id == "color":
            current_color = self.color_option_label(self.current_visual["color_id"]) if self.current_visual.get("color_id") else self.tr("default_color")
            draft_color = self.color_option_label(self.draft_visual["color_id"]) if self.draft_visual.get("color_id") else self.tr("default_color")
            if self.color_changed():
                return f"{current_color} -> {draft_color}"
            return draft_color
        if item_id == "nickname":
            current_name = str(self.current_visual.get("name") or self.tr("value_unknown"))
            draft_name = str(self.draft_visual.get("name") or current_name)
            if self.nickname_changed():
                return f"{current_name} -> {draft_name}"
            return draft_name
        if item_id == "apply":
            return self.tr("menu_state_pending") if self.has_pending_changes() else self.tr("menu_state_clean")
        if item_id == "restore":
            return self.tr("menu_state_restore_ready") if self.has_restore_target() else self.tr("menu_state_restore_empty")
        return ""

    def menu_detail_lines(self, width: int) -> list[str]:
        width = max(12, width)
        if self.screen == "main":
            item_id = TOP_LEVEL_MENU[self.selection["main"]]
            if item_id == "language":
                return [
                    self.tr("detail_language")[:width],
                    f"{self.tr('selected_language')}: {self.language_option_label(str(self.settings.get('language_id') or 'en'))}"[:width],
                ]
            if item_id == "color":
                current_color = self.color_option_label(self.current_visual["color_id"]) if self.current_visual.get("color_id") else self.tr("default_color")
                draft_color = self.color_option_label(self.draft_visual["color_id"]) if self.draft_visual.get("color_id") else self.tr("default_color")
                return [
                    self.tr("detail_color")[:width],
                    f"{self.tr('current')}: {current_color}"[:width],
                    f"{self.tr('draft')}: {draft_color}"[:width],
                ]
            if item_id == "nickname":
                current_name = str(self.current_visual.get("name") or self.tr("value_unknown"))
                draft_name = str(self.draft_visual.get("name") or current_name)
                return [
                    self.tr("detail_nickname")[:width],
                    f"{self.tr('current')}: {current_name}"[:width],
                    f"{self.tr('draft')}: {draft_name}"[:width],
                ]
            if item_id == "apply":
                return [
                    self.tr("detail_apply")[:width],
                    f"{self.tr('changes_label')}: {', '.join(self.draft_change_labels()) or self.tr('changes_none')}"[:width],
                    f"{self.tr('status_pending_changes')}: {self.tr('status_yes') if self.has_pending_changes() else self.tr('status_no')}"[:width],
                ]
            if item_id == "restore":
                return [
                    self.tr("detail_restore")[:width],
                    f"{self.tr('status_restore')}: {self.tr('status_yes') if self.has_restore_target() else self.tr('status_no')}"[:width],
                ]
            return [self.tr("detail_quit")[:width]]
        if self.screen == "language":
            label = self.language_option_label(LANGUAGE_ORDER[self.selection["language"]])
            return [
                f"{self.tr('selected_language')}: {label}"[:width],
                self.tr("detail_language_hint")[:width],
            ]
        if self.screen == "color":
            entry = self.color_menu_entries()[self.selection["color"]]
            color_options = {
                item["color_id"]: item
                for item in self.inspection["customization"]["color_options"]
            }
            option = color_options.get(entry["color_id"], {})
            status = self.tr("available") if entry["available"] else self.tr("unavailable")
            reason = str(option.get("reason") or "").strip()
            lines = [
                f"{self.tr('detail_color_status')}: {status}"[:width],
            ]
            if reason:
                lines.append(f"{self.tr('detail_color_reason')}: {reason}"[:width])
            return lines
        if self.screen == "nickname":
            return [self.tr("detail_nickname_hint")[:width]]
        return []

    def show_result(
        self,
        title_key: str,
        status: str,
        detail: str,
        next_step: str | None = None,
        summary_lines: list[str] | None = None,
    ) -> None:
        self.result_card = {
            "title_key": title_key,
            "status": status,
            "detail": detail,
            "next_step": next_step,
            "summary_lines": summary_lines or [],
        }
        self.screen = "result"

    def ensure_color_pairs(self) -> None:
        if self.color_pairs_ready or not curses.has_colors():
            return
        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass
        mapping = {
            "green": curses.COLOR_GREEN,
            "orange": curses.COLOR_YELLOW,
            "blue": curses.COLOR_BLUE,
            "pink": curses.COLOR_MAGENTA,
            "purple": curses.COLOR_MAGENTA,
            "red": curses.COLOR_RED,
            "black": curses.COLOR_BLACK,
            "white": curses.COLOR_WHITE,
        }
        pair_id = 1
        for color_id, color_value in mapping.items():
            try:
                curses.init_pair(pair_id, color_value, -1)
            except curses.error:
                continue
            pair_id += 1
        self.color_pairs_ready = True

    def color_attr(self, color_id: str | None) -> int:
        if not curses.has_colors():
            return 0
        mapping = {
            "green": 1,
            "orange": 2,
            "blue": 3,
            "pink": 4,
            "purple": 5,
            "red": 6,
            "black": 7,
            "white": 8,
        }
        pair_id = mapping.get(color_id)
        if not pair_id:
            return 0
        try:
            return curses.color_pair(pair_id)
        except curses.error:
            return 0

    def save_language(self, language_id: str) -> None:
        update_customization_settings(language_id=language_id)
        self.refresh()
        self.selection["language"] = self.current_language_index()
        self.set_message(self.tr("saved_language"))

    def save_color(self, color_id: str | None) -> None:
        if color_id is None:
            update_customization_settings(clear_color=True)
            self.refresh()
            self.selection["color"] = self.current_color_index()
            self.set_message(self.tr("clear_color_saved"))
            return
        update_customization_settings(color_id=color_id)
        self.refresh()
        self.selection["color"] = self.current_color_index()
        self.set_message(self.tr("saved_color"))

    def clear_nickname(self) -> None:
        update_customization_settings(clear_nickname=True)
        self.refresh()
        self.nickname_buffer = ""
        self.set_message(self.tr("cleared_nickname"))

    def save_nickname(self, nickname: str) -> None:
        nickname = nickname.strip()
        if nickname:
            update_customization_settings(nickname=nickname)
            self.set_message(self.tr("saved_nickname"))
        else:
            update_customization_settings(clear_nickname=True)
            self.set_message(self.tr("cleared_nickname"))
        self.refresh()

    def format_color_value(self, color_id: str | None) -> str:
        if color_id:
            return self.color_option_label(color_id)
        return self.tr("default_color")

    def result_summary_lines(
        self,
        before_visual: dict[str, Any],
        after_visual: dict[str, Any],
    ) -> list[str]:
        lines: list[str] = []
        before_name = before_visual.get("name") or self.tr("value_unknown")
        after_name = after_visual.get("name") or self.tr("value_unknown")
        if before_name != after_name:
            lines.append(f"{self.tr('display_name')}: {before_name} -> {after_name}")

        before_color = self.format_color_value(before_visual.get("color_id"))
        after_color = self.format_color_value(after_visual.get("color_id"))
        if before_color != after_color:
            lines.append(f"{self.tr('selected_color')}: {before_color} -> {after_color}")
        return lines

    def do_apply(self) -> None:
        try:
            before_visual = dict(self.current_visual)
            self.sync_hidden_element_setting()
            apply_installed_patch()
            self.refresh()
            self.set_message(self.tr("apply_success"))
            self.show_result(
                "result_apply_title",
                "ok",
                self.tr("apply_success"),
                self.tr("result_restart_needed"),
                self.result_summary_lines(before_visual, self.current_visual),
            )
        except Exception as exc:  # noqa: BLE001
            detail = f"{self.tr('action_failed')}: {exc}"
            self.set_message(detail)
            self.show_result("result_error_title", "error", detail)

    def do_restore(self) -> None:
        try:
            before_visual = dict(self.current_visual)
            restore_native_patch()
            self.refresh()
            self.set_message(self.tr("restore_success"))
            self.show_result(
                "result_restore_title",
                "ok",
                self.tr("restore_success"),
                self.tr("result_restore_ready"),
                self.result_summary_lines(before_visual, self.current_visual),
            )
        except Exception as exc:  # noqa: BLE001
            detail = f"{self.tr('action_failed')}: {exc}"
            self.set_message(detail)
            self.show_result("result_error_title", "error", detail)

    def submenu_count(self, screen: str) -> int:
        if screen == "language":
            return len(LANGUAGE_ORDER)
        if screen == "color":
            return len(self.color_menu_entries())
        if screen == "main":
            return len(TOP_LEVEL_MENU)
        return 0

    def render(self, stdscr: Any) -> None:
        stdscr.erase()
        self.ensure_color_pairs()
        height, width = stdscr.getmaxyx()
        if self.screen == "result":
            self.render_result(stdscr, height, width)
            stdscr.refresh()
            return
        menu_width = min(34, max(28, width // 3))
        divider_x = menu_width + 4

        stdscr.addstr(0, 2, self.tr("title"), curses.A_BOLD)
        stdscr.addstr(1, 2, self.tr("subtitle"))
        stdscr.addstr(0, divider_x, self.tr("preview"), curses.A_BOLD)
        buddy_name = self.current_visual.get("name") or self.tr("value_unknown")
        buddy_species = self.current_visual.get("species") or self.tr("value_unknown")
        status_line = (
            f"{self.tr('buddy_identity')}: {buddy_name} / {buddy_species}   "
            f"{self.tr('status_pending_changes')}: {self.tr('status_yes') if self.has_pending_changes() else self.tr('status_no')}   "
            f"{self.tr('status_restore')}: {self.tr('status_yes') if self.has_restore_target() else self.tr('status_no')}"
        )
        self.safe_addstr(stdscr, 2, 2, status_line[: max(0, width - 4)], curses.A_DIM)

        self.render_menu(stdscr, 4, 2, menu_width, height - 7)
        self.render_preview(stdscr, 4, divider_x, width - divider_x - 2, height - 7)

        help_text = {
            "main": self.tr("help_main"),
            "language": self.tr("help_submenu"),
            "color": self.tr("help_submenu"),
            "nickname": self.tr("help_input"),
            "result": self.tr("help_result"),
        }.get(self.screen, self.tr("help_main"))
        message = self.message or self.tr("restart_note")
        self.safe_addstr(stdscr, height - 2, 2, help_text[: max(0, width - 4)])
        self.safe_addstr(stdscr, height - 1, 2, message[: max(0, width - 4)])
        stdscr.refresh()

    def safe_addstr(self, stdscr: Any, y: int, x: int, text: str, attr: int = 0) -> None:
        try:
            stdscr.addstr(y, x, text, attr)
        except curses.error:
            pass

    def safe_hline(self, stdscr: Any, y: int, x: int, width: int) -> None:
        if width <= 0:
            return
        try:
            stdscr.hline(y, x, curses.ACS_HLINE, width)
        except curses.error:
            self.safe_addstr(stdscr, y, x, "-" * width)

    def safe_box(self, stdscr: Any, start_y: int, start_x: int, width: int, height: int) -> None:
        if width < 2 or height < 2:
            return
        for y in range(height):
            for x in range(width):
                ch = " "
                if y == 0 and x == 0:
                    ch = "+"
                elif y == 0 and x == width - 1:
                    ch = "+"
                elif y == height - 1 and x == 0:
                    ch = "+"
                elif y == height - 1 and x == width - 1:
                    ch = "+"
                elif y == 0 or y == height - 1:
                    ch = "-"
                elif x == 0 or x == width - 1:
                    ch = "|"
                self.safe_addstr(stdscr, start_y + y, start_x + x, ch)

    def render_preview_card(
        self,
        stdscr: Any,
        start_y: int,
        start_x: int,
        width: int,
        title: str,
        name_line: str,
        meta_line: str,
        color_line: str,
        footer_line: str,
        preview_lines: list[str],
        attr: int,
    ) -> None:
        card_height = 11
        self.safe_box(stdscr, start_y, start_x, width, card_height)
        self.safe_addstr(stdscr, start_y + 1, start_x + 2, title[: max(0, width - 4)], curses.A_BOLD)
        self.safe_addstr(stdscr, start_y + 2, start_x + 2, name_line[: max(0, width - 4)])
        self.safe_addstr(stdscr, start_y + 3, start_x + 2, meta_line[: max(0, width - 4)], curses.A_DIM)
        self.safe_addstr(stdscr, start_y + 4, start_x + 2, color_line[: max(0, width - 4)], attr)
        self.safe_hline(stdscr, start_y + 5, start_x + 1, max(0, width - 2))
        row = start_y + 6
        for line in preview_lines[:3]:
            self.safe_addstr(stdscr, row, start_x + 2, line[: max(0, width - 4)], attr)
            row += 1
        self.safe_addstr(stdscr, start_y + card_height - 2, start_x + 2, footer_line[: max(0, width - 4)], curses.A_DIM)

    def render_menu(self, stdscr: Any, start_y: int, start_x: int, width: int, height: int) -> None:
        self.safe_box(stdscr, start_y, start_x, width, max(6, height))
        inner_x = start_x + 2
        inner_width = max(8, width - 4)
        section_title = {
            "main": self.tr("menu_header"),
            "language": self.tr("screen_language"),
            "color": self.tr("screen_color"),
            "nickname": self.tr("screen_nickname"),
        }.get(self.screen, self.tr("menu_header"))
        self.safe_addstr(stdscr, start_y + 1, inner_x, section_title, curses.A_BOLD)
        self.safe_hline(stdscr, start_y + 2, start_x + 1, max(6, width - 2))
        lines: list[tuple[str, bool, int]] = []
        if self.screen == "main":
            selected = self.selection["main"]
            for index, item_id in enumerate(TOP_LEVEL_MENU):
                label = self.top_level_label(item_id)
                value = self.main_menu_value(item_id)
                if item_id == "color" and self.color_changed():
                    value = f"{value} [{self.tr('draft')}]"
                elif item_id == "nickname" and self.nickname_changed():
                    value = f"{value} [{self.tr('draft')}]"
                marker = "›" if index == selected else " "
                text = f"{marker} {label}: {value}" if value else f"{marker} {label}"
                attr = 0
                if item_id in {"color", "nickname"}:
                    if (item_id == "color" and self.color_changed()) or (item_id == "nickname" and self.nickname_changed()):
                        attr = curses.A_BOLD
                if item_id == "apply":
                    attr = curses.A_BOLD if self.has_pending_changes() else curses.A_DIM
                elif item_id == "restore" and not self.has_restore_target():
                    attr = curses.A_DIM
                lines.append((text, index == selected, attr))
            lines.append(("", False, 0))
            lines.append(
                (
                    f"{self.tr('status_pending_changes')}: {self.tr('status_yes') if self.has_pending_changes() else self.tr('status_no')}",
                    False,
                    0,
                )
            )
            lines.append(
                (
                    f"{self.tr('status_restore')}: {self.tr('status_yes') if self.has_restore_target() else self.tr('status_no')}",
                    False,
                    0,
                )
            )
        elif self.screen == "language":
            selected = self.selection["language"]
            for index, language_id in enumerate(LANGUAGE_ORDER):
                label = self.language_option_label(language_id)
                if self.settings.get("language_id") == language_id:
                    label = f"{label} [{self.tr('current')}]"
                marker = "›" if index == selected else " "
                lines.append((f"{marker} {label}", index == selected, 0))
        elif self.screen == "color":
            self.safe_addstr(stdscr, start_y + 3, inner_x, self.tr("color_menu_hint")[:inner_width])
            selected = self.selection["color"]
            preview_visual = self.preview_draft_visual()
            for index, entry in enumerate(self.color_menu_entries()):
                color_id = entry["color_id"]
                marker = "›" if index == selected else " "
                label = f"{marker} {self.color_chip(color_id)} {entry['label']}"
                suffix = []
                if self.settings.get("color_id") == color_id:
                    suffix.append(self.tr("current"))
                if preview_visual.get("color_id") == color_id and self.current_visual.get("color_id") != color_id:
                    suffix.append(self.tr("draft"))
                if not entry["available"]:
                    suffix.append(self.tr("unavailable"))
                elif color_id is not None:
                    suffix.append(self.tr("available"))
                if suffix:
                    label = f"{label} [{' / '.join(suffix)}]"
                lines.append((label, index == selected, self.color_attr(color_id)))
        elif self.screen == "nickname":
            lines.append(
                (
                    f"{self.tr('nickname_current')}: {self.current_visual.get('name') or self.tr('value_unknown')}",
                    False,
                    0,
                )
            )
            lines.append(
                (
                    f"{self.tr('nickname_draft')}: {self.settings.get('nickname') or self.tr('value_none')}",
                    False,
                    0,
                )
            )
            lines.append(("", False, 0))
            lines.append((self.tr("nickname_prompt"), False, 0))
            buffer = self.nickname_buffer
            if not buffer:
                buffer = self.settings.get("nickname") or ""
            lines.append((f"› {self.tr('nickname_input')}: {buffer or '…'}", True, 0))

        detail_lines = self.menu_detail_lines(inner_width)
        detail_block_height = (len(detail_lines) + 2) if detail_lines else 0
        y = start_y + (5 if self.screen == "color" else 4)
        max_list_lines = max(0, height - 5 - detail_block_height)
        for text, highlighted, base_attr in lines[: max_list_lines]:
            attr = base_attr | (curses.A_REVERSE if highlighted else 0)
            self.safe_addstr(stdscr, y, inner_x, text[:inner_width], attr)
            y += 1
        if detail_lines:
            detail_y = start_y + height - detail_block_height
            self.safe_hline(stdscr, detail_y, start_x + 1, max(6, width - 2))
            self.safe_addstr(stdscr, detail_y + 1, inner_x, self.tr("detail_header")[:inner_width], curses.A_BOLD)
            row = detail_y + 2
            for line in detail_lines[: max(0, height - row + start_y - 1)]:
                self.safe_addstr(stdscr, row, inner_x, line[:inner_width], curses.A_DIM)
                row += 1

    def render_preview(self, stdscr: Any, start_y: int, start_x: int, width: int, height: int) -> None:
        customization = self.inspection.get("customization") or {}
        current_profile = self.inspection.get("current_profile") or {}
        preview_visual = self.preview_draft_visual()
        draft_element = preview_visual.get("element_id") or self.tr("value_none")
        current_element = current_profile.get("element_id") or self.current_visual.get("element_id") or self.tr("value_none")
        lines = [
            f"- {self.tr('selected_language')}: {self.language_option_label(str(self.settings.get('language_id') or 'en'))}",
            f"- {self.tr('apply_ready')}: {self.tr('status_yes') if bool(self.inspection.get('profile_match')) else self.tr('status_no')}",
            f"- {self.tr('changes_label')}: {', '.join(self.draft_change_labels(preview_visual)) or self.tr('changes_none')}",
            f"- {self.tr('status_pending_changes')}: {self.tr('status_yes') if self.has_pending_changes(preview_visual) else self.tr('status_no')}",
            f"- {self.tr('status_restore')}: {self.tr('status_yes') if self.has_restore_target() else self.tr('status_no')}",
        ]
        warnings = customization.get("apply_warnings") or []
        blockers = customization.get("apply_blockers") or []
        if warnings:
            lines.append(f"- {self.tr('pending')}: {warnings[0]}")
        elif blockers:
            lines.append(f"- {blockers[0]}")

        summary_height = 9
        self.safe_box(stdscr, start_y, start_x, width, summary_height)
        self.safe_addstr(stdscr, start_y + 1, start_x + 2, self.tr("summary_header")[: max(0, width - 4)], curses.A_BOLD)
        self.safe_hline(stdscr, start_y + 2, start_x + 1, max(0, width - 2))
        y = start_y + 3
        for line in lines[: max(0, summary_height - 4)]:
            self.safe_addstr(stdscr, y, start_x + 2, line[: max(0, width - 4)])
            y += 1

        box_width = max(24, min(width, 30))
        box_height = 11

        installed_color_line = f"{self.color_chip(self.current_visual.get('color_id'))} {self.color_option_label(self.current_visual['color_id']) if self.current_visual.get('color_id') else self.tr('default_color')}"
        current_attr = self.color_attr(self.current_visual.get("color_id"))
        draft_color_line = f"{self.color_chip(preview_visual.get('color_id'))} {self.color_option_label(preview_visual['color_id']) if preview_visual.get('color_id') else self.tr('default_color')}"
        draft_attr = self.color_attr(preview_visual.get("color_id"))
        y = start_y + summary_height + 1
        self.render_preview_card(
            stdscr,
            y,
            start_x,
            box_width,
            f"{self.tr('installed_preview')} [{self.tr('current')}]",
            self.current_visual.get("name") or self.tr("value_unknown"),
            f"{self.tr('buddy_identity')}: {self.current_visual.get('species') or self.tr('value_unknown')}",
            installed_color_line,
            f"{self.tr('installed_element')}: {current_element}",
            list(self.current_visual.get("preview_lines") or []),
            current_attr,
        )

        y += box_height + 1
        self.render_preview_card(
            stdscr,
            y,
            start_x,
            box_width,
            f"{self.tr('draft_preview')} [{self.tr('draft') if self.has_pending_changes(preview_visual) else self.tr('current')}]",
            preview_visual.get("name") or self.tr("value_unknown"),
            f"{self.tr('changes_label')}: {', '.join(self.draft_change_labels(preview_visual)) or self.tr('changes_none')}",
            draft_color_line,
            f"{self.tr('selected_nickname')}: {preview_visual.get('name') if preview_visual.get('name') != self.current_visual.get('name') else self.tr('value_none')}",
            list(preview_visual.get("preview_lines") or []),
            draft_attr,
        )

    def render_result(self, stdscr: Any, height: int, width: int) -> None:
        card = self.result_card or {}
        title = self.tr(card.get("title_key") or "result_error_title")
        status = str(card.get("status") or "info").upper()
        detail = str(card.get("detail") or self.tr("value_unknown"))
        next_step = card.get("next_step")
        summary_lines = list(card.get("summary_lines") or [])

        body = [
            (title, curses.A_BOLD),
            ("", 0),
            (f"{self.tr('result_status')}: {status}", curses.A_BOLD if status == "OK" else 0),
            (detail, 0),
        ]
        if summary_lines:
            body.append(("", 0))
            body.extend((line, 0) for line in summary_lines)
        if next_step:
            body.extend(
                [
                    ("", 0),
                    (f"{self.tr('result_next_step')}: {next_step}", 0),
                ]
            )
        body.extend(
            [
                ("", 0),
                (self.tr("result_return_hint"), curses.A_DIM),
            ]
        )

        max_line = max(len(text) for text, _ in body)
        box_w = min(max(width - 8, 20), max_line + 6)
        box_h = len(body) + 4
        start_y = max(1, (height - box_h) // 2)
        start_x = max(2, (width - box_w) // 2)

        for y in range(box_h):
            for x in range(box_w):
                ch = " "
                if y == 0 and x == 0:
                    ch = "+"
                elif y == 0 and x == box_w - 1:
                    ch = "+"
                elif y == box_h - 1 and x == 0:
                    ch = "+"
                elif y == box_h - 1 and x == box_w - 1:
                    ch = "+"
                elif y == 0 or y == box_h - 1:
                    ch = "-"
                elif x == 0 or x == box_w - 1:
                    ch = "|"
                self.safe_addstr(stdscr, start_y + y, start_x + x, ch)

        y = start_y + 2
        for text, attr in body:
            self.safe_addstr(stdscr, y, start_x + 2, text[: max(0, box_w - 4)], attr)
            y += 1

    def handle_key(self, key: Any) -> None:
        if self.screen == "nickname":
            self.handle_nickname_key(key)
            return
        if self.screen == "result":
            if key in ("q", "Q", 27, curses.KEY_ENTER, 10, 13):
                self.screen = "main"
                self.result_card = None
            return

        if key in ("q", "Q", 27):
            if self.screen == "main":
                self.running = False
            else:
                self.screen = "main"
            return

        if key == curses.KEY_UP:
            size = self.submenu_count(self.screen)
            if size:
                self.selection[self.screen] = (self.selection[self.screen] - 1) % size
            return

        if key == curses.KEY_DOWN:
            size = self.submenu_count(self.screen)
            if size:
                self.selection[self.screen] = (self.selection[self.screen] + 1) % size
            return

        if key in (curses.KEY_ENTER, 10, 13):
            self.activate_current()

    def activate_current(self) -> None:
        if self.screen == "main":
            item_id = TOP_LEVEL_MENU[self.selection["main"]]
            if item_id in {"language", "color"}:
                self.screen = item_id
                if item_id == "language":
                    self.selection["language"] = self.current_language_index()
                if item_id == "color":
                    self.selection["color"] = self.current_color_index()
            elif item_id == "nickname":
                self.screen = "nickname"
                self.nickname_buffer = str(self.settings.get("nickname") or "")
            elif item_id == "apply":
                if not self.has_pending_changes():
                    self.set_message(self.tr("message_no_pending_changes"))
                    return
                self.do_apply()
            elif item_id == "restore":
                if not self.has_restore_target():
                    self.set_message(self.tr("message_no_restore"))
                    return
                self.do_restore()
            elif item_id == "quit":
                self.running = False
            return

        if self.screen == "language":
            self.save_language(LANGUAGE_ORDER[self.selection["language"]])
            self.screen = "main"
            return

        if self.screen == "color":
            entry = self.color_menu_entries()[self.selection["color"]]
            if not entry["available"]:
                self.set_message(f"{self.tr('action_failed')}: {entry['label']} ({self.tr('unavailable')})")
                return
            self.save_color(entry["color_id"])
            self.screen = "main"

    def handle_nickname_key(self, key: Any) -> None:
        if key == 27:
            self.screen = "main"
            self.nickname_buffer = ""
            return
        if key in (curses.KEY_ENTER, 10, 13):
            self.save_nickname(self.nickname_buffer)
            self.nickname_buffer = ""
            self.screen = "main"
            return
        if key in (curses.KEY_BACKSPACE, 127, 8, "\b", "\x7f"):
            self.nickname_buffer = self.nickname_buffer[:-1]
            return
        if isinstance(key, str) and key not in ("\n", "\r", "\t"):
            self.nickname_buffer += key

    def run(self, stdscr: Any) -> None:
        curses.curs_set(0)
        stdscr.keypad(True)
        while self.running:
            self.render(stdscr)
            key = stdscr.get_wch()
            self.handle_key(key)


def dump_language(language_id: str) -> int:
    if language_id not in LANGUAGE_PACKS:
        raise SystemExit(f"Unknown language: {language_id}")
    pack = LANGUAGE_PACKS[language_id]
    print(pack["menu_language"])
    print(pack["menu_color"])
    print(pack["menu_nickname"])
    print(pack["menu_apply"])
    print(pack["menu_restore"])
    print(pack["menu_quit"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="BuddyHub standalone TUI")
    parser.add_argument("--dump-language", choices=sorted(LANGUAGE_PACKS.keys()))
    parser.add_argument("--dump-state", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.dump_language:
        return dump_language(args.dump_language)
    if args.dump_state:
        app = BuddyHubTUI()
        print(
            json.dumps(
                {
                    "settings": app.settings,
                    "current_visual": app.current_visual,
                    "draft_visual": app.draft_visual,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    app = BuddyHubTUI()
    curses.wrapper(app.run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
