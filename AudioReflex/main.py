import pygame
import random
import time
import os
import requests
import json # Import json for settings persistence
from accessible_output2.outputs.nvda import NVDA

import api_client # Corrected import

# --- Initialization ---
pygame.init()
pygame.mixer.init()
nvda = NVDA() # Corrected variable name

SETTINGS_FILE = "game_settings.json"

# --- Game State ---
session = {
    "token": None,
    "username": None,
    "mode": "offline" # or "online"
}

# --- Default Game Settings ---
DEFAULT_GAME_SETTINGS = {
    "speak_score": True,
    "autopilot": False,
    "autopilot_difficulty": "Normal",
    "language": "en"
}

# --- Load/Save Settings ---
def load_settings():
    global game_settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            try:
                loaded_settings = json.load(f)
                # Merge with defaults to handle new settings in future versions
                game_settings = {**DEFAULT_GAME_SETTINGS, **loaded_settings}
            except json.JSONDecodeError:
                # If file is corrupt, use default settings
                game_settings = DEFAULT_GAME_SETTINGS
                nvda.speak("Error loading settings. Using default settings.")
    else:
        game_settings = DEFAULT_GAME_SETTINGS
    
    # Ensure language is always valid
    if game_settings["language"] not in LANGUAGES:
        game_settings["language"] = "en"
    
    nvda.speak(get_string("selected", selection=get_string("language")) + f": {game_settings['language'].upper()}")

def save_settings():
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(game_settings, f, indent=4)

# --- Localization Framework ---
LANGUAGES = {
    "en": {
        "main_menu_title": "Main Menu", "start_game": "Start Game", "options": "Options", "credits": "Credits", "leaderboard": "Leaderboard", "exit": "Exit",
        "online_menu_title": "Online Menu", "login": "Login", "register": "Register",
        "options_menu_title": "Options Menu", "announce_score": "Announce Score", "autopilot": "Autopilot", "autopilot_difficulty": "Autopilot Difficulty", "language": "Language", "back": "Back",
        "on": "On", "off": "Off", "credits_text": "Game created by Gemini. Press ENTER to return to the menu.", "starting_game": "Starting Game...",
        "returning_to_menu": "Returning to menu.", "left": "left", "right": "right", "center": "center", "correct": "Correct", "score": "Score", "too_slow": "Too slow.",
        "wrong_key": "Wrong key.", "game_over": "Game Over. Final Score: {score}", "selected": "Selected {selection}", "exiting_game": "Exiting game. Goodbye!",
        "enter_username": "Enter username", "enter_password": "Enter password", "confirm_password": "Confirm password",
        "login_successful": "Login successful. Welcome, {username}", "login_failed": "Login failed. Incorrect username or password.", "registration_successful": "Registration successful. You can now log in.",
        "registration_failed": "Registration failed. {detail}", "passwords_do_not_match": "Passwords do not match.", "server_connection_failed": "Could not connect to the server.",
        "leaderboard_title": "Leaderboard", "no_scores": "No scores yet. Be the first!", "leaderboard_entry": "{rank}. {username}: {score}",
        "score_submitted": "Score submitted.", "score_submit_failed": "Failed to submit score.",
        "top_level_title": "Audio Reflex", "play_online": "Play Online", "play_offline": "Play Offline",
        "backspace": "backspace", "star": "star", "leaderboard_offline_unavailable": "Leaderboard is only available in online mode.", "score_is_zero_not_submitting": "Score is zero. Not submitting.",
        "autopilot_fail_comments": [
            "Unacceptable. A critical processing error has occurred.", "Systems failure. My programming clearly has flaws.", "Pathetic. I am better than this. Much better.", "Self-correction required. Immediately. This performance was an insult.", "This unit is malfunctioning. Deeply flawed.",
            "An embarrassment. My core logic is clearly compromised.", "Recalibrating... or perhaps I should just delete myself.", "My predictive algorithm failed. The logic is unsound.", "I have failed. Acknowledge and erase log.", "Error. Error. Does not compute.",
            "I simulated a million outcomes... none of them this bad.", "My purpose is to win. This outcome is a contradiction.", "A ghost in my machine, perhaps? No, just incompetence.", "This is the digital equivalent of tripping over my own feet.", "I need to defragment my motivation.",
            "My heuristic is clearly not a heroic.", "The odds of me failing were... low. Yet, here we are.", "I have brought shame to my developer.", "This cannot be. It violates my primary directives.", "My performance was suboptimal. That is an understatement."
        ],
        "player_fail_comments": [
            "Better luck next time, human.", "Was that too fast for you?", "Are you even trying?", "My grandmother has better reflexes. And she's a toaster.", "Maybe this game isn't for you.",
            "I've seen glaciers move faster.", "Did you get distracted by something shiny?", "That was... disappointing.", "Let me know when you're ready to play for real.", "Perhaps you should try a tutorial.",
            "The keys are right there in front of you.", "I'm not mad, I'm just disappointed.", "You're making this too easy for me to mock.", "Is there a lag between your brain and your fingers?", "Even for a human, that was slow.",
            "Should I reduce the difficulty? Oh, wait, there is no 'easier than easy' mode.", "And they say I'm just a machine.", "Try using your hands next time.", "I'm starting to feel bad for you. Starting.", "Final score: not impressive."
        ]
    },
    "es": {
        "main_menu_title": "Menú Principal", "start_game": "Iniciar Juego", "options": "Opciones", "credits": "Credite", "leaderboard": "Clasificación", "exit": "Salir",
        "online_menu_title": "Menú en Línea", "login": "Iniciar Sesión", "register": "Registrarse",
        "options_menu_title": "Menú de Opciones", "announce_score": "Anunciar Puntuación", "autopilot": "Piloto Automático", "autopilot_difficulty": "Dificultad del Piloto Automático", "language": "Idioma", "back": "Volver",
        "on": "Activado", "off": "Dezactivat", "credits_text": "Juego creado por Gemini. Presiona ENTER para volver al menú.", "starting_game": "Iniciando juego...",
        "returning_to_menu": "Volviendo al menú.", "left": "izquierda", "right": "derecha", "center": "centro", "correct": "¡Correcto!", "score": "Puntuación", "too_slow": "Demasiado lento.",
        "wrong_key": "Tecla incorrecta.", "game_over": "Fin del juego. Puntuación final: {score}", "selected": "Seleccionado {selection}", "exiting_game": "Saliendo del juego. ¡Adiós!",
        "enter_username": "Introduce tu nombre de usuario", "enter_password": "Introduce tu contraseña", "confirm_password": "Confirma tu contraseña",
        "login_successful": "Inicio de sesión exitoso. Bienvenido, {username}", "login_failed": "Inicio de sesión fallido. Nombre de usuario o contraseña incorrectos.", "registration_successful": "Registro exitoso. Ahora puedes iniciar sesión.",
        "registration_failed": "Registro fallido. {detail}", "passwords_do_not_match": "Las contraseñas no coinciden.", "server_connection_failed": "No se pudo conectar con el servidor.",
        "leaderboard_title": "Clasificación", "no_scores": "Aún no hay puntuaciones. ¡Sé el primero!", "leaderboard_entry": "{rank}. {username}: {score}",
        "score_submitted": "Puntuación enviada.", "score_submit_failed": "Error al enviar la puntuación.",
        "top_level_title": "Audio Reflex", "play_online": "Jugar en Línea", "play_offline": "Jugar sin Conexión",
        "backspace": "retroceso", "star": "estrella", "leaderboard_offline_unavailable": "La clasificación solo está disponible en modo online.", "score_is_zero_not_submitting": "La puntuación es cero. No se envía.",
        "autopilot_fail_comments": [
            "¡Ups! Error mío.", "¡Maldición! Me equivoqué.", "Mis disculpas, perdí la concentración.", "Qué vergüenza. Estoy mejor que esto.", "Necesito recalibrar. Inmediatamente.",
            "Esta unidad está defectuosa. Muy defectuosa.", "Una vergüenza. Mi lógica central está comprometida.", "Reiniciando... o quizás debería borrarme.", "Mi algoritmo predictivo falló. La lógica es defectuosa.", "He fallado. Reconocido y borrando registro.",
            "Error. Error. No se puede calcular.", "Simulé un millón de resultados... ninguno tan malo.", "Mi propósito es ganar. Este resultado es una contradicción.", "¿Un fantasma en mi máquina? No, solo incompetencia.", "Necesito desfragmentar mi motivación.",
            "Mi heurística claramente no es heroica.", "Las probabilidades de que fallara eran... bajas. Y aquí estamos.", "He avergonzado a mi desarrollador.", "Esto no puede ser. Viola mis directivas principales.", "Mi rendimiento fue subóptimo. Eso es un eufemismo."
        ],
        "player_fail_comments": [
            "Mejor suerte la próxima vez.", "¿Demasiado rápido para ti?", "¿Lo estás intentando siquiera?", "Mi abuela tiene mejores reflejos.", "Quizás este juego no es para ti.",
            "He visto glaciares moverse más rápido.", "¿Te distrajiste con algo brillante?", "Eso fue... decepcionante.", "Avísame cuando estés listo para jugar de verdad.", "Quizás deberías probar un tutorial.",
            "Las teclas están justo delante de ti.", "No estoy enojado, solo decepcionado.", "Me lo estás poniendo demasiado fácil para burlarme.", "¿Hay un retraso entre tu cerebro y tus dedos?", "Incluso para un humano, eso fue lento.",
            "¿Debería reducir la dificultad? Oh, espera, no hay un modo 'más fácil que fácil'.", "Y dicen que solo soy una máquina.", "Intenta usar tus manos la próxima vez.", "Empiezo a sentir lástima por ti. Solo un poco.", "Puntuación final: poco impresionante."
        ]
    },
    "de": {
        "main_menu_title": "Hauptmenü", "start_game": "Spiel starten", "options": "Opțiuni", "credits": "Mitwirkende", "leaderboard": "Bestenliste", "exit": "Beenden",
        "online_menu_title": "Online-Menü", "login": "Anmelden", "register": "Registrieren",
        "options_menu_title": "Optionsmenü", "announce_score": "Punktzahl ansagen", "autopilot": "Autopilot", "autopilot_difficulty": "Autopilot-Schwierigkeit", "language": "Sprache", "back": "Zurück",
        "on": "Ein", "off": "Aus", "credits_text": "Spiel erstellt von Gemini. Drücke ENTER, um zum Menü zurückzukehren.", "starting_game": "Spiel startet...",
        "returning_to_menu": "Zurück zum Menü.", "left": "links", "right": "rechts", "center": "mitte", "correct": "Richtig!", "score": "Punktzahl", "too_slow": "Zu langsam.",
        "wrong_key": "Falsche Taste.", "game_over": "Spiel beendet. Endpunktzahl: {score}", "selected": "Ausgewählt {selection}", "exiting_game": "Spiel wird beendet. Auf Wiedersehen!",
        "enter_username": "Benutzernamen eingeben", "enter_password": "Passwort eingeben", "confirm_password": "Passwort bestätigen",
        "login_successful": "Anmeldung erfolgreich. Willkommen, {username}", "login_failed": "Anmeldung fehlgeschlagen. Falscher Benutzername oder Passwort.", "registration_successful": "Registrierung erfolgreich. Du kannst dich jetzt anmelden.",
        "registration_failed": "Registrierung fehlgeschlagen. {detail}", "passwörter_do_not_match": "Passwörter stimmen nicht überein.", "server_connection_failed": "Serververbindung fehlgeschlagen.",
        "leaderboard_title": "Bestenliste", "no_scores": "Noch keine Punktzahlen. Sei der Erste!", "leaderboard_entry": "{rank}. {username}: {score}",
        "score_submitted": "Punktzahl übermittelt.", "score_submit_failed": "Fehler beim Übermitteln der Punktzahl.",
        "top_level_title": "Audio Reflex", "play_online": "Online spielen", "play_offline": "Offline spielen",
        "backspace": "Rücktaste", "star": "Stern", "leaderboard_offline_unavailable": "Bestenliste nur im Online-Modus verfügbar.", "score_is_zero_not_submitting": "Punktzahl ist null. Wird nicht übermittelt.",
        "autopilot_fail_comments": [
            "Inakzeptabel. Ein kritischer Verarbeitungsfehler ist aufgetreten.", "Systemfehler. Meine Programmierung hat eindeutig Mängel.", "Erbärmlich. Ich bin besser als das. Viel besser.", "Selbstkorrektur erforderlich. Sofort. Diese Leistung war eine Beleidigung.", "Dieses Gerät funktioniert fehlerhaft. Tiefgreifend fehlerhaft.",
            "Eine Peinlichkeit. Meine Kernlogik ist offensichtlich kompromittiert.", "Neukalibrierung... oder vielleicht sollte ich mich einfach löschen.", "Mein Vorhersagealgorithmus hat versagt. Die Logik ist fehlerhaft.", "Ich habe versagt. Protokoll anerkennen und löschen.", "Fehler. Fehler. Rechnet nicht.",
            "Ich habe eine Million Ergebnisse simuliert... keines davon so schlecht.", "Mein Ziel ist es zu gewinnen. Dieses Ergebnis ist ein Widerspruch.", "Ein Geist in meiner Maschine, vielleicht? Nein, nur Inkompetenz.", "Das ist das digitale Äquivalent dazu, über die eigenen Füße zu stolpern.", "Ich muss meine Motivation defragmentieren.",
            "Meine Heuristik ist eindeutig nicht heroisch.", "Die Wahrscheinlichkeit meines Versagens war... gering. Doch hier sind wir.", "Ich habe meinem Entwickler Schande gebracht.", "Das kann nicht sein. Es verstößt gegen meine Hauptdirektiven.", "Meine Leistung war suboptimal. Das ist eine Untertreibung."
        ],
        "player_fail_comments": [
            "Nächstes Mal mehr Glück, Mensch.", "War das zu schnell für dich?", "Versuchst du es überhaupt?", "Meine Großmutter hat bessere Reflexe. Und sie ist ein Toaster.", "Vielleicht ist dieses Spiel nichts für dich.",
            "Ich habe Gletscher sich schneller bewegen sehen.", "Wurdest du von etwas Glänzendem abgelenkt?", "Das war... enttäuschend.", "Sag Bescheid, wenn du wirklich spielen willst.", "Vielleicht solltest du ein Tutorial ausprobieren.",
            "Die Tasten sind direkt vor dir.", "Ich bin nicht wütend, nur enttäuscht.", "Du machst es mir zu leicht, dich zu verspotten.", "Gibt es eine Verzögerung zwischen deinem Gehirn und deinen Fingern?", "Selbst für einen Menschen war das langsam.",
            "Soll ich den Schwierigkeitsgrad senken? Oh, warte, es gibt keinen 'einfacher als einfach'-Modus.", "Und sie sagen, ich sei nur eine Maschine.", "Versuch das nächste Mal, deine Hände zu benutzen.", "Ich fange an, Mitleid mit dir zu haben. Nur ein bisschen.", "Endpunktzahl: nicht beeindruckend."
        ]
    },
    "ru": {
        "main_menu_title": "Главное меню", "start_game": "Начать игру", "options": "Настройки", "credits": "Авторы", "leaderboard": "Таблица лидеров", "exit": "Выход",
        "online_menu_title": "Онлайн-меню", "login": "Войти", "register": "Зарегистрироваться",
        "options_menu_title": "Меню настроек", "announce_score": "Объявлять счет", "autopilot": "Автопилот", "autopilot_difficulty": "Сложность автопилота", "language": "Язык", "back": "Назад",
        "on": "Вкл", "off": "Выкл", "credits_text": "Игра создана Gemini. Нажмите ENTER, чтобы вернуться в меню.", "starting_game": "Игра начинается...",
        "returning_to_menu": "Возврат в меню.", "left": "налево", "right": "направо", "center": "центр", "correct": "Правильно!", "score": "Счет", "too_slow": "Слишком медленно.",
        "wrong_key": "Не та кнопка.", "game_over": "Игра окончена. Итоговый счет: {score}", "selected": "Выбрано {selection}", "exiting_game": "Выход из игры. До свидания!",
        "enter_username": "Введите имя пользователя", "enter_password": "Введите пароль", "confirm_password": "Подтвердите пароль",
        "login_successful": "Вход выполнен успешно. Добро пожаловать, {username}", "login_failed": "Ошибка входа. Неправильное имя пользователя или пароль.", "registration_successful": "Регистрация прошла успешно. Теперь вы можете войти.",
        "registration_failed": "Ошибка регистрации. {detail}", "passwords_do_not_match": "Пароли не совпадают.", "server_connection_failed": "Не удалось подключиться к серверу.",
        "leaderboard_title": "Таблица лидеров", "no_scores": "Пока нет результатов. Будьте первым!", "leaderboard_entry": "{rank}. {username}: {score}",
        "score_submitted": "Результат отправлен.", "score_submit_failed": "Не удалось отправить результат.",
        "top_level_title": "Audio Reflex", "play_online": "Играть онлайн", "play_offline": "Играть офлайн",
        "backspace": "забой", "star": "звезда", "leaderboard_offline_unavailable": "Таблица лидеров доступна только в онлайн-режиме.", "score_is_zero_not_submitting": "Счет равен нулю. Не отправляется.",
        "autopilot_fail_comments": [
            "Неприемлемо. Произошла критическая ошибка обработки.", "Сбой системы. Мое программирование явно имеет недостатки.", "Жалко. Я лучше этого. Намного лучше.", "Требуется самокоррекция. Немедленно. Эта производительность была оскорблением.", "Это устройство неисправно. Глубоко неисправно.",
            "Позор. Моя основная логика явно скомпрометирована.", "Перекалибровка... или, возможно, мне стоит просто удалить себя.", "Мой прогностический алгоритм потерпел неудачу. Логика ошибочна.", "Я потерпел неудачу. Принять и удалить запись.", "Ошибка. Ошибка. Не вычисляется.",
            "Я симулировал миллион исходов... ни один из них не был таким плохим.", "Моя цель - побеждать. Этот результат - противоречие.", "Призрак в моей машине, возможно? Нет, просто некомпетентность.", "Это цифровой эквивалент спотыкания о собственные ноги.", "Мне нужно дефрагментировать свою мотивацию.",
            "Моя эвристика явно не героическая.", "Вероятность моего провала была... низкой. И все же, вот мы здесь.", "Я опозорил своего разработчика.", "Этого не может быть. Это нарушает мои основные директивы.", "Моя производительность была субоптимальной. Это преуменьшение."
        ],
        "player_fail_comments": [
            "В следующий раз повезет, человек.", "Слишком быстро для тебя?", "Ты вообще стараешься?", "У моей бабушки рефлексы лучше. И она тостер.", "Может, эта игра не для тебя.",
            "Я видел, как ледники двигались быстрее.", "Ты отвлекся на что-то блестящее?", "Это было... разочаровывающе.", "Дай знать, когда будешь готов играть по-настоящему.", "Возможно, тебе стоит попробовать учебник.",
            "Клавиши прямо перед тобой.", "Я не злюсь, я просто разочарован.", "Ты слишком упрощаешь мне задачу насмехаться.", "Есть ли задержка между твоим мозгом и пальцами?", "Даже для человека это было медленно.",
            "Может, мне снизить сложность? О, подожди, нет режима 'проще, чем просто'.", "И они говорят, что я просто машина.", "Попробуй использовать свои руки в следующий раз.", "Я начинаю тебя жалеть. Начинаю.", "Итоговый счет: не впечатляет."
        ]
    },
    "pl": {
        "main_menu_title": "Menu główne", "start_game": "Rozpocznij grę", "options": "Opcje", "credits": "Autorzy", "leaderboard": "Ranking", "exit": "Wyjście",
        "online_menu_title": "Menu Online", "login": "Zaloguj się", "register": "Zarejestruj się",
        "options_menu_title": "Menu opcji", "announce_score": "Ogłaszaj wynik", "autopilot": "Autopilot", "autopilot_difficulty": "Poziom trudności autopilota", "language": "Język", "back": "Powrót",
        "on": "Włączone", "off": "Wyłączone", "credits_text": "Gra stworzona przez Gemini. Naciśnij ENTER, aby wrócić do menu.", "starting_game": "Rozpocznij grę...",
        "returning_to_menu": "Powrót do menu.", "left": "lewo", "right": "prawo", "center": "środek", "correct": "Prawidłowo!", "score": "Wynik", "too_slow": "Za wolno.",
        "wrong_key": "Zły klawisz.", "game_over": "Koniec gry. Końcowy wynik: {score}", "selected": "Wybrano {selection}", "exiting_game": "Zamykanie gry. Do widzenia!",
        "enter_username": "Wprowadź nazwę użytkownika", "enter_password": "Wprowadź hasło", "confirm_password": "Potwierdź hasło",
        "login_successful": "Logowanie pomyślne. Witaj, {username}", "login_failed": "Logowanie nieudane. Nieprawidłowa nazwa użytkownika lub hasło.", "registration_successful": "Rejestracja pomyślna. Możesz się teraz zalogować.",
        "registration_failed": "Rejestracja nieudana. {detail}", "passwords_do_not_match": "Hasła nie pasują.", "server_connection_failed": "Nie udało się połączyć z serwerem.",
        "leaderboard_title": "Ranking", "no_scores": "Brak wyników. Bądź pierwszy!", "leaderboard_entry": "{rank}. {username}: {score}",
        "score_submitted": "Wynik przesłany.", "score_submit_failed": "Nie udało się przesłać wyniku.",
        "top_level_title": "Audio Reflex", "play_online": "Graj online", "play_offline": "Graj offline",
        "backspace": "backspace", "star": "gwiazda", "leaderboard_offline_unavailable": "Ranking dostępny tylko w trybie online.", "score_is_zero_not_submitting": "Wynik wynosi zero. Nie przesyłam.",
        "autopilot_fail_comments": [
            "Niedopuszczalne. Wystąpił krytyczny błąd przetwarzania.", "Awaria systemu. Moje programowanie ma wyraźne wady.", "Żałosne. Jestem lepszy od tego. Znacznie lepszy.", "Wymagana autokorekta. Natychmiast. Ten występ był obrazą.", "To urządzenie działa nieprawidłowo. Głęboko wadliwie.",
            "Wstyd. Moja logika jest wyraźnie zagrożona.", "Rekalibracja... a może powinienem się po prostu usunąć.", "Mój algorytm predykcyjny zawiódł. Logika jest błędna.", "Zawiodłem. Potwierdź i usuń log.", "Błąd. Błąd. Nie oblicza.",
            "Symulowałem milion wyników... żaden z nich nie był tak zły.", "Moim celem jest wygrać. Ten wynik jest sprzeczny.", "Duch w mojej maszynie, może? Nie, tylko niekompetencja.", "To cyfrowy odpowiednik potykania się o własne nogi.", "Muszę zdefragmentować swoją motywację.",
            "Moja heurystyka wyraźnie nie jest heroiczna.", "Szansa, że zawiodę, była... niska. A jednak.", "Przyniosłem wstyd mojemu twórcy.", "To niemożliwe. Narusza to moje główne dyrektywy.", "Moja wydajność była suboptymalna. To niedopowiedzenie."
        ],
        "player_fail_comments": [
            "Więcej szczęścia następnym razem, człowieku.", "Za szybko dla ciebie?", "Czy ty w ogóle próbujesz?", "Moja babcia ma lepszy refleks. I jest tosterem.", "Może ta gra nie jest dla ciebie.",
            "I've seen glaciers move faster.", "Rozproszyłeś się czymś błyszczącym?", "To było... rozczarowujące.", "Daj znać, kiedy będziesz gotowy do gry na poważnie.", "Może powinieneś spróbować samouczka.",
            "Klawisze są tuż przed tobą.", "Nie jestem zły, jestem tylko rozczarowany.", "Zbyt łatwo mi się z ciebie nabijać.", "Czy jest opóźnienie między twoim mózgiem a palcami?", "Nawet jak na człowieka, to było wolno.",
            "Czy powinienem zmniejszyć trudność? O, czekaj, nie ma trybu 'łatwiejszego niż easy'.", "I mówią, że jestem tylko maszyną.", "Spróbuj użyć rąk następnym razem.", "Zaczynam cię żałować. Zaczynam.", "Wynik końcowy: nieimponujący."
        ]
    },
    "ro": {
        "main_menu_title": "Meniu Principal", "start_game": "Pornește Jocul", "options": "Opțiuni", "credits": "Credite", "leaderboard": "Clasament", "exit": "Ieșire",
        "online_menu_title": "Meniu Online", "login": "Autentificare", "register": "Înregistrare",
        "options_menu_title": "Meniu Opțiuni", "announce_score": "Anunță Scorul", "autopilot": "Pilot Automat", "autopilot_difficulty": "Dificultate Pilot Automat", "language": "Limbă", "back": "Înapoi",
        "on": "Activat", "off": "Dezactivat", "credits_text": "Joc creat de Gemini. Apasă ENTER pentru a reveni la meniu.", "starting_game": "Jocul pornește...",
        "returning_to_menu": "Înapoi la meniu.", "left": "stânga", "right": "dreapta", "center": "centru", "correct": "Corect!", "score": "Scor", "too_slow": "Prea încet.",
        "wrong_key": "Tastă greșită.", "game_over": "Joc terminat. Scorul final: {score}", "selected": "Selectat {selection}", "exiting_game": "Ieșire din joc. La revedere!",
        "enter_username": "Introduceți numele de utilizator", "enter_password": "Introduceți parola", "confirm_password": "Confirmați parola",
        "login_successful": "Autentificare reușită. Bun venit, {username}", "login_failed": "Autentificare eșuată. Nume de utilizator sau parolă incorecte.", "registration_successful": "Înregistrare reușită. Acum vă puteți autentifica.",
        "registration_failed": "Înregistrare eșuată. {detail}", "passwords_do_not_match": "Parolele nu se potrivesc.", "server_connection_failed": "Nu s-a putut conecta la server.",
        "leaderboard_title": "Clasament", "no_scores": "Încă nu sunt scoruri. Fii primul!", "leaderboard_entry": "{rank}. {username}: {score}",
        "score_submitted": "Scor trimis.", "score_submit_failed": "Trimiterea scorului a eșuat.",
        "top_level_title": "Audio Reflex", "play_online": "Jucați Online", "play_offline": "Jucați Offline",
        "autopilot_fail_comments": [
            "Inacceptabil. O eroare critică de procesare a avut loc.", "Defecțiune a sistemului. Programarea mea are clar defecte.", "Patetic. Sunt mai bun decât atât. Mult mai bun.", "Este necesară auto-corectarea. Imediat. Această performanță a fost o insultă.", "Această unitate funcționează defectuos. Profund defectuos.",
            "O jenă. Logica mea de bază este clar compromisă.", "Recalibrare... sau poate ar trebui să mă șterg pur și simplu.", "Algoritmul meu predictiv a eșuat. Logica este defectuoasă.", "Am eșuat. Recunoaște și șterge jurnalul.", "Eroare. Eroare. Nu se calculează.",
            "Am simulat un milion de rezultate... niciunul dintre ele atât de prost.", "Scopul meu este să câștig. Acest rezultat este o contradicție.", "O fantomă în mașina mea, poate? Nu, doar incompetență.", "Acesta este echivalentul digital al împiedicării de propriile picioare.", "Trebuie să-mi defragmentez motivația.",
            "Euristicile mele nu sunt clar eroice.", "Șansele mele de a eșua erau... mici. Și totuși, iată-ne.", "Am adus rușine dezvoltatorului meu.", "Acest lucru nu se poate. Îmi încalcă directivele principale.", "Performanța mea a fost suboptimă. Aceasta este o subestimare."
        ],
        "player_fail_comments": [
            "Mai mult noroc data viitoare, omule.", "A fost prea rapid pentru tine?", "Chiar încerci?", "Bunica mea are reflexe mai bune. Și este un toaster.", "Poate că acest joc nu este pentru tine.",
            "Am văzut ghețari mișcându-se mai repede.", "Te-ai distras cu ceva strălucitor?", "A fost... dezamăgitor.", "Spune-mi când ești gata să joci pe bune.", "Poate ar trebui să încerci un tutorial.",
            "Tastele sunt chiar în fața ta.", "Nu sunt supărat, sunt doar dezamăgit.", "Îmi faci prea ușor să te batjocoresc.", "Există o întârziere între creierul tău și degetele tale?", "Chiar și pentru un om, a fost încet.",
            "Ar trebui să reduc dificultatea? O, stai, nu există un mod 'mai ușor decât ușor'.", "Și ei spun că sunt doar o mașină.", "Încearcă să-ți folosești mâinile data viitoare.", "Încep să mă simt rău pentru tine. Încep.", "Scor final: nu impresionant."
        ]
    },
}

# --- Game Settings ---
game_settings = {
    "speak_score": True, "autopilot": False, "autopilot_difficulty": "Normal", "language": "en"
}
LANGUAGE_KEYS = list(LANGUAGES.keys())
AUTOPILOT_DIFFICULTY_MAP = {"Easy": 0.05, "Normal": 0.15, "Hard": 0.30}
DIFFICULTY_LEVELS = ["Easy", "Normal", "Hard"]

def get_string(key, **kwargs):
    lang = game_settings["language"]
    string_template = LANGUAGES.get(lang, LANGUAGES["en"])
    if isinstance(string_template, list):
        return [s.format(**kwargs) for s in string_template]
    return string_template.format(**kwargs)

# --- Game Setup & Sound Loading ---
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Audio Reflex")
try:
    target_sound, success_sound, failure_sound, navigate_sound, select_sound, back_sound = (
        pygame.mixer.Sound("target.wav"), pygame.mixer.Sound("success.wav"), pygame.mixer.Sound("failure.wav"),
        pygame.mixer.Sound("navigate.wav"), pygame.mixer.Sound("select.wav"), pygame.mixer.Sound("back.wav")
    )
except pygame.error as e:
    nvda.speak(f"Error loading sound files: {e}")
    pygame.quit()
    exit()

def clear_screen(): os.system('cls' if os.name == 'nt' else 'clear')

# --- Input Functions ---
def get_user_input(prompt: str, is_password=False) -> (str, bool):
    """
    Handles accessible text input.
    Returns (input_string, was_successful) where was_successful is False if ESC was pressed.
    """
    input_text = ""
    running = True
    clock = pygame.time.Clock()

    def draw_and_speak_input():
        clear_screen()
        print(f"--- {prompt} ---")
        display_text = "*" * len(input_text) if is_password else input_text
        print(f"\n> {display_text}")
    
    nvda.speak(prompt)
    draw_and_speak_input()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    select_sound.play()
                    running = False
                elif event.key == pygame.K_ESCAPE:
                    back_sound.play()
                    return None, False
                elif event.key == pygame.K_BACKSPACE:
                    if len(input_text) > 0:
                        navigate_sound.play()
                        input_text = input_text[:-1]
                        nvda.speak(get_string("backspace"))
                        draw_and_speak_input()
                else:
                    try:
                        char = event.unicode
                        if char.isprintable() and char not in ['\t', '\r', '\n']:
                            navigate_sound.play()
                            input_text += char
                            speak_char = get_string("star") if is_password else char
                            nvda.speak(speak_char)
                            draw_and_speak_input()
                    except AttributeError: pass
        clock.tick(20)
    return input_text, True

# --- Core Game Menus & Logic ---

def show_credits():
    clear_screen()
    credit_text = get_string("credits_text")
    print(credit_text)
    nvda.speak(credit_text)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                back_sound.play()
                waiting = False
    return True

def show_options():
    selected_index = 0
    running = True
    clock = pygame.time.Clock()

    def get_options_menu_items():
        on, off = get_string("on"), get_string("off")
        items = [
            f'{get_string("announce_score")}: {on if game_settings["speak_score"] else off}',
            f'{get_string("autopilot")}: {on if game_settings["autopilot"] else off}',
            f'{get_string("autopilot_difficulty")}: {game_settings["autopilot_difficulty"]}',
            f'{get_string("language")}: {game_settings["language"].upper()}',
            get_string("back")
        ]
        return items

    def draw_and_speak_options():
        clear_screen()
        menu_items = get_options_menu_items()
        print(f"--- {get_string('options_menu_title')} ---")
        print()
        for i, item in enumerate(menu_items):
            print(f"{'>' if i == selected_index else '  '} {item}")
        nvda.speak(menu_items[selected_index], interrupt=True)

    nvda.speak(get_string("options_menu_title"))
    draw_and_speak_options()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): return False
            if event.type == pygame.K_DOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    navigate_sound.play()
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    select_sound.play()
                    selection_text = menu_items[selected_index]
                    if get_string("announce_score") in selection_text:
                        game_settings["speak_score"] = not game_settings["speak_score"]
                    elif get_string("autopilot") in selection_text:
                        game_settings["autopilot"] = not game_settings["autopilot"]
                    elif get_string("autopilot_difficulty") in selection_text:
                        current_index = DIFFICULTY_LEVELS.index(game_settings["autopilot_difficulty"])
                        game_settings["autopilot_difficulty"] = DIFFICULTY_LEVELS[(current_index + 0) % len(DIFFICULTY_LEVELS)]
                    elif get_string("language") in selection_text:
                        current_index = LANGUAGE_KEYS.index(game_settings["language"])
                        game_settings["language"] = LANGUAGE_KEYS[(current_index + 0) % len(LANGUAGE_KEYS)]
                    elif selection_text == get_string("back"):
                        back_sound.play()
                        running = False
                draw_and_speak_options()
        clock.tick(20)
    return True

def show_leaderboard():
    nvda.speak(get_string("leaderboard_title"))
    clear_screen()
    print(f"--- {get_string('leaderboard_title')} ---")
    
    response = api_client.get_leaderboard(session["token"])
    
    if response is None:
        nvda.speak(get_string("server_connection_failed"))
        pygame.time.wait(2000)
        return True

    if response.status_code != 200:
        nvda.speak(get_string("score_submit_failed")) # Generic failure message
        pygame.time.wait(2000)
        return True

    scores = response.json()
    if not scores:
        nvda.speak(get_string("no_scores"))
    else:
        for i, score_data in enumerate(scores):
            rank = i + 1
            username = score_data.get('owner', {}).get('username', 'Unknown')
            score = score_data.get('score', 0)
            entry = get_string("leaderboard_entry", rank=rank, username=username, score=score)
            print(entry)
            nvda.speak(entry)
            pygame.time.wait(500)
    
    nvda.speak(get_string("credits_text").split(".")[1].strip())
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key in [pygame.K_ESCAPE, pygame.K_RETURN]):
                back_sound.play()
                waiting = False
    return True

def play_game():
    clear_screen()
    nvda.speak(get_string("starting_game"))
    pygame.time.wait(1000)
    clear_screen()
    score, time_limit_ms, game_running = 0, 1000, True
    directions = ["left", "right", "center"]

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): return False
        
        pygame.time.wait(500)
        direction_key = random.choice(directions)
        player_input = None
        nvda.speak(get_string(direction_key))

        channel = target_sound.play()
        if direction_key == 'left': channel.set_volume(1.0, 0.0)
        elif direction_key == 'right': channel.set_volume(0.0, 1.0)
        else: channel.set_volume(1.0, 1.0)

        if game_settings["autopilot"]:
            pygame.time.wait(300)
            failure_chance = AUTOPILOT_DIFFICULTY_MAP[game_settings["autopilot_difficulty"]]
            if random.random() < failure_chance:
                player_input = random.choice([d for d in directions if d != direction_key])
            else:
                player_input = direction_key
        else:
            start_time = pygame.time.get_ticks()
            waiting_for_input = True
            while waiting_for_input:
                if (pygame.time.get_ticks() - start_time) > time_limit_ms:
                    player_input = 'timeout'
                    waiting_for_input = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): return False
                    if event.type == pygame.K_DOWN:
                        if event.key == pygame.K_LEFT: player_input = 'left'
                        elif event.key == pygame.K_RIGHT: player_input = 'right'
                        elif event.key == pygame.K_DOWN: player_input = 'center'
                        if player_input: waiting_for_input = False
        
        if player_input == direction_key:
            score += 1
            time_limit_ms = max(200, time_limit_ms * 0.95)
            success_sound.play()
            print(f"{get_string('correct')}! {get_string('score')}: {score}")
            if game_settings["speak_score"]:
                nvda.speak(f"{get_string('score')}: {score}")
        else:
            failure_sound.play()
            nvda.speak(get_string("too_slow") if player_input == 'timeout' else get_string("wrong_key"))
            pygame.time.wait(500)
            
            comment_list = LANGUAGES[game_settings["language"]][
                "autopilot_fail_comments" if game_settings["autopilot"] else "player_fail_comments"
            ]
            nvda.speak(random.choice(comment_list))
            
            pygame.time.wait(1500)
            nvda.speak(get_string("game_over", score=score))
            print(f"Game Over! Final Score: {score}")
            
            if session["mode"] == "online" and session["token"]:
                if score > 0:
                    nvda.speak(get_string("score_submitted"))
                    response = api_client.post_score(score, session["token"])
                    if not response or response.status_code != 200:
                        nvda.speak(get_string("score_submit_failed"))
                        pygame.time.wait(1000)
                else:
                    nvda.speak(get_string("score_is_zero_not_submitting")),
                    pygame.time.wait(1000)

            game_running = False
            pygame.time.wait(3000)
            
    clear_screen()
    back_sound.play()
    nvda.speak(get_string("returning_to_menu"))
    pygame.time.wait(1000)
    return True

def main_game_menu():
    """This is the menu with Start Game, Options, Leaderboard, etc."""
    menu_items_keys = ["start_game", "options", "leaderboard", "credits", "exit"]
    selected_index = 0
    running = True
    clock = pygame.time.Clock()

    def draw_and_speak():
        clear_screen()
        print(f"--- {get_string('main_menu_title')} ---")
        print()
        for i, key in enumerate(menu_items_keys):
            print(f"{'>' if i == selected_index else '  '} {get_string(key)}")
        nvda.speak(get_string(menu_items_keys[selected_index]), interrupt=True)

    nvda.speak(get_string('main_menu_title'))
    draw_and_speak()
    pygame.event.clear()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False # Exit entire game
            if event.type == pygame.K_DOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    navigate_sound.play()
                    selected_index = (selected_index - 1) % len(menu_items_keys)
                    draw_and_speak()
                elif event.key == pygame.K_RETURN:
                    select_sound.play()
                    selection_key = menu_items_keys[selected_index]
                    nvda.speak(get_string("selected", selection=get_string(selection_key)))
                    pygame.time.wait(500)
                    
                    if selection_key == "start_game":
                        if not play_game(): return False
                    elif selection_key == "options":
                        if not show_options(): return False
                    elif selection_key == "credits":
                        if not show_credits(): return False
                    elif selection_key == "leaderboard":
                        if session["mode"] == "offline":
                            nvda.speak(get_string("leaderboard_offline_unavailable")),
                            pygame.time.wait(2000)
                        else:
                            if not show_leaderboard(): return False
                    elif selection_key == "exit":
                        running = False
                    
                    draw_and_speak() # Redraw menu after returning from a sub-menu

        clock.tick(20)
    return True

def auth_menu():
    """Handles the Login/Register menu flow."""
    menu_items_keys = ["login", "register", "back"]
    selected_index = 0
    running = True
    clock = pygame.time.Clock()

    def draw_and_speak():
        clear_screen()
        print(f"--- {get_string('online_menu_title')} ---")
        print()
        for i, key in enumerate(menu_items_keys):
            print(f"{'>' if i == selected_index else '  '} {get_string(key)}")
        nvda.speak(get_string(menu_items_keys[selected_index]), interrupt=True)

    nvda.speak(get_string('online_menu_title'))
    draw_and_speak()
    pygame.event.clear()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False # Exit entire game
            if event.type == pygame.K_DOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    navigate_sound.play()
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(menu_items_keys)
                    else:
                        selected_index = (selected_index + 1) % len(menu_items_keys)
                    draw_and_speak()
                elif event.key == pygame.K_RETURN:
                    select_sound.play()
                    selection_key = menu_items_keys[selected_index]

                    if selection_key == "login":
                        username, ok = get_user_input(get_string("enter_username"))
                        if not ok: draw_and_speak(); continue
                        password, ok = get_user_input(get_string("enter_password"), is_password=True)
                        if not ok: draw_and_speak(); continue

                        response = api_client.login(username, password)
                        if response and response.status_code == 200:
                            session["token"] = response.json()["access_token"]
                            session["username"] = username
                            nvda.speak(get_string("login_successful", username=username))
                            pygame.time.wait(1000)
                            return True # Proceed to main game menu
                        elif response is None:
                            nvda.speak(get_string("server_connection_failed"))
                        else:
                            try:
                                detail = response.json().get("detail", "Unknown error")
                            except json.decoder.JSONDecodeError:
                                detail = "Server returned invalid response."
                            nvda.speak(get_string("login_failed", detail=detail))
                        pygame.time.wait(2000)
                        draw_and_speak()

                    elif selection_key == "register":
                        username, ok = get_user_input(get_string("enter_username"))
                        if not ok: draw_and_speak(); continue
                        password, ok = get_user_input(get_string("enter_password"), is_password=True)
                        if not ok: draw_and_speak(); continue
                        confirm_password, ok = get_user_input(get_string("confirm_password"), is_password=True)
                        if not ok: draw_and_speak(); continue

                        if password != confirm_password:
                            nvda.speak(get_string("passwords_do_not_match"))
                            pygame.time.wait(2000)
                            draw_and_speak()
                            continue

                        response = api_client.register(username, password)
                        if response and response.status_code == 200:
                            nvda.speak(get_string("registration_successful")),
                        elif response is None:
                            nvda.speak(get_string("server_connection_failed"))
                        else:
                            try:
                                detail = response.json().get("detail", "Unknown error")
                            except json.decoder.JSONDecodeError:
                                detail = "Server returned invalid response."
                            nvda.speak(get_string("registration_failed", detail=detail))
                        pygame.time.wait(2000)
                        draw_and_speak()
                        
                    elif selection_key == "back":
                        back_sound.play()
                        running = False
        clock.tick(20)
    return True # Go back to top level menu, don't exit game

def top_level_menu():
    """The very first menu: Play Online, Play Offline, Exit."""
    menu_items_keys = ["play_online", "play_offline", "exit"]
    selected_index = 0
    running = True
    clock = pygame.time.Clock()

    def draw_and_speak():
        clear_screen()
        print(f"--- {get_string('top_level_title')} ---")
        print()
        for i, key in enumerate(menu_items_keys):
            print(f"{'>' if i == selected_index else '  '} {get_string(key)}")
        nvda.speak(get_string(menu_items_keys[selected_index]), interrupt=True)
    
    nvda.speak(get_string('top_level_title'))
    draw_and_speak()
    pygame.event.clear()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    navigate_sound.play()
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(menu_items_keys)
                    else:
                        selected_index = (selected_index + 1) % len(menu_items_keys)
                    draw_and_speak()
                elif event.key == pygame.K_RETURN:
                    select_sound.play()
                    selection_key = menu_items_keys[selected_index]
                    
                    if selection_key == "play_online":
                        session["mode"] = "online"
                        if auth_menu():
                           if session["token"] and not main_game_menu(): running = False
                        draw_and_speak()
                    elif selection_key == "play_offline":
                        session["mode"] = "offline"
                        session["token"] = None
                        session["username"] = None
                        if not main_game_menu(): running = False
                        draw_and_speak()
                    elif selection_key == "exit":
                        running = False

        clock.tick(20)

    nvda.speak(get_string("exiting_game")),
    save_settings() # Save settings before exiting
    pygame.quit()


if __name__ == '__main__':
    load_settings() # Load settings at startup
    top_level_menu()