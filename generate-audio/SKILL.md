---
name: "generate-audio"
description: "Generate a spoken WAV file from text with the local Kokoro text-to-speech service through the flux-klein MCP tool generate_speech, using a clickable wizard where the user types the text and an optional file name. Use when the user wants a voice memo, narration, read-aloud, voiceover, or speech file, or says generate audio, text to speech, read this aloud, or maak een audiobestand. Not for images."
---

# Generate audio (text to speech)

Turn text into a spoken WAV file. The skill collects the text, voice, speed, and file name through a short clickable wizard. As soon as the wizard is complete, it calls the text-to-speech tool on its own, saves the WAV file, and sends the file back into the conversation. This skill is for speech only. For images, use the flux-klein skill.

## Rules

- Use only the tool `mcp__remote-devices__flux-klein__generate_speech`. Never call an HTTP endpoint directly.
- The tool is synchronous. It returns the saved file path, voice, and byte count in the same call. No polling is needed.
- Speak the user's text exactly as given. Do not rewrite, summarise, or translate it unless the user asks.
- Once the wizard has the text, call the tool right away. Do not ask for a further confirmation.
- Always send the finished WAV file into the conversation with `SendUserFile`. Do not ask whether to send it.
- Do not ask a follow-up question after delivery, such as what to do next. End with the file and a short summary.
- Reply to the user in their language.
- The tool saves the file on the user's computer. Its path is on that computer, not in this chat.

## Step 1: Load the tool

Load it before anything else:

`ToolSearch` with query `select:mcp__remote-devices__flux-klein__generate_speech`

If the tool cannot be loaded, or the call fails with a connection error, tell the user that the text-to-speech service isn't reachable. The Claude desktop app must be open and linked to this chat on the computer that runs the service.

## Step 2: Run the wizard

If the user's request already contains the exact text to speak, use that text and skip the text question. Otherwise, call AskUserQuestion once with these four questions, in this order.

1. **Text** (header: "Text"). Question: "Type the exact text to speak in the Other box below." Options: "Type it in Other (Recommended)" with description "Select Other and type or paste the text.", and "Cancel" with description "Stop without generating audio." The text always comes from the user. Never invent or fill in text.
2. **Voice** (header: "Voice"). Question: "Which voice should read it?" Options: "af_heart (Recommended)", "af_bella", "am_adam", "bf_emma". The user can type another Kokoro voice ID through Other.
3. **Speed** (header: "Speed"). Question: "How fast should it be spoken?" Options: "Normal 1.0 (Recommended)", "Slower 0.8", "Faster 1.2". The user can type another number through Other.
4. **File name** (header: "File name"). Question: "Type the file name in the Other box, or keep the automatic name." Options: "Automatic name (Recommended)" with description "Use the name the tool generates.", and "Type a name in Other" with description "Select Other and type the file name, without .wav."

**Defaults:** If the user skips the voice or speed question, use the "(Recommended)" option. If the user skips the file name question, use the automatic name. The text has no default. If the text is empty or the user cancels, stop and say so. Do not generate audio without text.

If the user typed a name ending in .wav, remove the extension before using it. If the user typed a number for speed, use that number. If the user typed a voice ID, use it as written.

## Step 3: Check the input

Before calling the tool, confirm that the text is not empty and that the voice and speed have values. Use the defaults if needed. Keep the text as the user wrote it.

## Step 4: Generate

Call `generate_speech` immediately with:
- `text`: the user's text, unchanged
- `voice`: the chosen voice ID (default `af_heart`)
- `speed`: the chosen speed as a number (default `1`)

The result gives `path`, `voice`, and `bytes`. If the call fails, retry once. If a voice is rejected, retry once with `af_heart` and tell the user. If it fails again, report the error in plain words and suggest checking that the service is running.

## Step 5: Save and deliver

1. **Typed file name:** Use `mcp__remote-devices__device_bash` to rename the generated file in the same folder to the typed name plus `.wav`. If the device shell is not available, keep the generated name and say so. The shell only sees connected folders under `$HOME/mnt/`, so find the folder there first if a plain path fails. If the folder is not granted yet, request access once with `mcp__remote-devices__device_request_folder_access`.
2. **Stage the file:** Call `mcp__remote-devices__device_stage_files` with the file's path on the computer, using the final name.
3. **Send the file:** Call `SendUserFile` with the staged file, `display: "attach"`, and a short caption naming the voice and speed. The file card lets the user play or download the audio in the conversation.
4. **Reply:** In one or two sentences, say that the audio is attached, give the full path on the computer, and give the voice, speed, and approximate length.

Always do steps 1 to 4 for every audio file. Do not offer a next-step question after delivery.