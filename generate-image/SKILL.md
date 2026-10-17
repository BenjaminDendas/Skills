---
name: "generate-image"
description: "Generate an image from a text prompt using the local Flux Klein 4B service through the flux-klein MCP tools, then show it inline. Use this whenever the user wants to create, generate, make, draw, render, or design an image, picture, illustration, or photo, including phrases like \"create image\", \"create-image\", \"generate image\", \"generate-image\", \"make an image\", \"draw me\", \"picture of\", \"illustration of\", \"render this\", \"maak me een afbeelding\", \"maak een afbeelding\", \"genereer een afbeelding\", \"teken\", or \"foto van\". Also use it when the user types /flux-klein. Walks the user through a clickable wizard, builds an English prompt, calls the service, and shows the result. Always go through the MCP tools, never the FastAPI or any HTTP endpoint."
---
 
# Flux Klein image generation
 
Generate an image from a text-only prompt. There are no input images. The skill collects the user's choices through a short clickable wizard, turns them into one English prompt, calls the Flux Klein service through the MCP tools, and shows the result inline.
 
## Rules
 
- Always call the MCP tools `mcp__remote-devices__flux-klein__start_image_generation`, `mcp__remote-devices__flux-klein__get_image_result`, and `mcp__remote-devices__flux-klein__service_health`. Never call the FastAPI or any HTTP endpoint directly, even if the service URL is known.
- Generation is asynchronous. `start_image_generation` only starts a job and returns straight away. The image arrives later through `get_image_result`, which you poll every 10 seconds until the job is finished. Keep exactly 30 seconds between one poll and the next. Polling back to back, or every second, floods the service with requests and gains nothing, because the job takes much longer than that. Never treat the start call's response as the finished image.
- Width and height must each be 1024 or less. Use only the sizes listed in step 2, because larger images take too long to generate.
- The service takes only `prompt`, `width`, `height`, and `seed`. It has no negative prompt, so express exclusions in the prompt itself, such as "without any text" or "no people in the scene".
- Write the prompt in English, whatever language the user used. Reply to the user in their language.
- Do not save images to a specific folder. The image is shown in the chat and can be downloaded from there.
## Step 1: Load the tools and check the service
 
The Flux Klein tools are deferred. Load them in one call before anything else:
 
`ToolSearch` with query `select:mcp__remote-devices__flux-klein__start_image_generation,mcp__remote-devices__flux-klein__get_image_result,mcp__remote-devices__flux-klein__service_health`
 
Then call `service_health`. If it fails or reports the service is down, stop and tell the user that the Flux Klein service isn't running. The Claude desktop app must be open and linked to this chat on the computer that runs the service. Do not start the wizard until the health check passes.
 
## Step 2: Run the wizard
 
Use the AskUserQuestion tool. It allows at most four questions per call and two to four options per question, so ask in two rounds. The user can always type their own answer through "Other". Put the default first and label it "(Recommended)".
 
**Round 1**
 
1. **Subject** (header: "Subject"). Question: "What should the image show?" Options: "A person", "A place or landscape", "An object", "A scene with several things". The user types specifics through "Other".
2. **Style** (header: "Style"). Options: "Photorealistic (Recommended)", "Illustration", "Painting", "Other style". The user types 3D render, anime, or an artist reference through "Other".
3. **Composition** (header: "Composition"). Options: "Full scene (Recommended)", "Close-up", "Wide landscape", "Portrait framing".
4. **Mood and lighting** (header: "Mood"). Options: "Natural daylight (Recommended)", "Warm golden hour", "Moody and dark", "Bright and cheerful".
**Round 2**
 
5. **Colors** (header: "Colors"). Options: "No preference (Recommended)", "Warm tones", "Cool tones", "Muted pastels". The user types specific colors, or colors to avoid, through "Other".
6. **Details** (header: "Details"). Options: "None (Recommended)", "Include text in the image", "Leave out people", "Add a specific element". The user types the specifics through "Other".
7. **Size** (header: "Size"). Options:
   - "Square 1024x1024 (Recommended)"
   - "Portrait 640x960 (2:3)"
   - "Landscape 960x640 (3:2)"
   - "Wide 1024x576 (16:9)"
   The user can type "Portrait 576x1024 (9:16)" through "Other".
**Defaults:** If the user skips a question or gives no answer, use the "(Recommended)" option. Subject is the only exception. If it is empty, ask again before generating, because no sensible default exists.
 
## Step 3: Build the prompt
 
Combine the answers into one English phrase, most important first:
 
`[subject], [style], [composition], [mood and lighting], [colors], [details]`
 
- Translate the user's answers into English if needed.
- Put any text that must appear in quotes, for example: a sign that reads "OPEN".
- Turn exclusions into positive or "without" phrasing, since there is no negative prompt.
- Skip any part that is "No preference" or "None". Add no filler words.
## Step 4: Generate
 
Generation runs in two parts, because the service is asynchronous.
 
1. Call `start_image_generation` with:
   - `prompt`: the prompt from step 3
   - `width` and `height`: from the chosen size
   - `seed`: leave it out unless the user asks for a specific seed
   This returns a job, not an image. Keep the job identifier it returns, since `get_image_result` needs it. Check the tool's schema for the exact name of that identifier.
2. Poll `get_image_result` with that identifier every 10 seconds. While the job is still running, keep polling, and tell the user briefly that the image is being generated. Stop once the result reports the job is complete, or has failed. Do not give up because one poll shows it is still working.
If starting the job fails, report the error in plain words and retry once. If the job itself fails, or the start call fails again, tell the user and suggest they check that the service is running.
 
## Step 5: Show the result
 
Send the generated image with `SendUserFile`, using `display: "render"` so it appears inline. The file card also lets the user download it, so no separate download step is needed.
 
Add a short caption with the size. Then write a one-line reply that gives the English prompt used and the seed, so the user can see what was sent and can reproduce or tweak the result.
 
## Step 6: Offer the next step
 
Use AskUserQuestion once:
- "Keep this one" (ends the flow)
- "Tweak one thing" (the user types the change, and the skill regenerates with an edited prompt and the same seed so the rest stays similar)
- "Start over" (return to step 2)
When tweaking, reuse the seed from the previous run. If the service did not report a seed, pick a fixed number and use it for the rerun.