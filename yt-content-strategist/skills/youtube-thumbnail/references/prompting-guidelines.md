# Prompting Guide and Strategies

Mastering Gemini image generation starts with one fundamental principle:

> **Describe the scene, don't just list keywords.** The model's core strength is its deep language understanding. A narrative, descriptive paragraph will almost always produce a better, more coherent image than a list of disconnected words.

---

## Model Selection

**Gemini 3 Pro Image Preview (Nano Banana Pro)** is the default and recommended model. Use it for most tasks.

| Feature | Pro (Default) | Flash |
|---------|---------------|-------|
| Resolution | 1K / 2K / 4K | 1K only |
| Max Input Images | 14 | 3 |
| Text Rendering | Advanced | Good |
| "Thinking" Process | Yes (refines composition) | No |
| Google Search Grounding | Yes | No |
| Speed | Slower | Faster |

**When to use Flash instead:**
- High-volume, low-latency tasks where speed matters more than quality
- Simple generations that don't need advanced features
- Cost-sensitive batch operations

---

## Prompts for Generating Images

The following strategies will help you create effective prompts to generate exactly the images you're looking for.

### 1. Photorealistic Scenes

For realistic images, use photography terms. Mention camera angles, lens types, lighting, and fine details to guide the model toward a photorealistic result.

**Template:**
```
A photorealistic [shot type] of [subject], [action or expression], set in
[environment]. The scene is illuminated by [lighting description], creating
a [mood] atmosphere. Captured with a [camera/lens details], emphasizing
[key textures and details]. The image should be in a [aspect ratio] format.
```

### 2. Stylized Illustrations & Stickers

To create stickers, icons, or assets, be explicit about the style and request a transparent background.

**Template:**
```
A [style] sticker of a [subject], featuring [key characteristics] and a
[color palette]. The design should have [line style] and [shading style].
The background must be transparent.
```

### 3. Accurate Text in Images

Gemini excels at rendering text. Be clear about the text, the font style (descriptively), and the overall design.

**Template:**
```
Create a [image type] for [brand/concept] with the text "[text to render]"
in a [font style]. The design should be [style description], with a
[color scheme].
```

### 4. Product Mockups & Commercial Photography

Perfect for creating clean, professional product shots for e-commerce, advertising, or branding.

**Template:**
```
A high-resolution, studio-lit product photograph of a [product description]
on a [background surface/description]. The lighting is a [lighting setup,
e.g., three-point softbox setup] to [lighting purpose]. The camera angle is
a [angle type] to showcase [specific feature]. Ultra-realistic, with sharp
focus on [key detail]. [Aspect ratio].
```

### 5. Minimalist & Negative Space Design

Excellent for creating backgrounds for websites, presentations, or marketing materials where text will be overlaid.

**Template:**
```
A minimalist composition featuring a single [subject] positioned in the
[bottom-right/top-left/etc.] of the frame. The background is a vast, empty
[color] canvas, creating significant negative space. Soft, subtle lighting.
[Aspect ratio].
```

### 6. Sequential Art (Comic Panel / Storyboard)

Builds on character consistency and scene description to create panels for visual storytelling. **Best with Pro model** for accurate text and complex compositions.

**Template:**
```
Make a [number] panel comic in a [art style] style. Put the character in
a [type of scene]. [Additional style details like contrast, inks, colors].
```

---

## Gemini 3 Pro-Specific Features

These features are only available with the Pro model.

### 1. Character Consistency (360° Views)

Create consistent multi-angle views of the same character by including previously generated images in follow-up prompts.

**Template:**
```
A studio portrait of [person/character] against [background],
[looking forward/in profile looking right/from behind/etc.]
```

**Tip:** For complex poses, include a reference image showing the desired pose along with your character reference.

### 2. Sketch-to-Photo ("Bring to Life")

Upload a rough sketch and transform it into a polished, realistic image.

**Template:**
```
Turn this rough [medium] sketch of a [subject] into a [style description]
photo. Keep the [specific features] from the sketch but add
[new details/materials/lighting].
```

**Example prompt:**
```
Turn this rough pencil sketch of a futuristic car into a polished photo of
the finished concept car in a showroom. Keep the sleek lines and low profile
from the sketch but add metallic blue paint and neon rim lighting.
```

### 3. High-Resolution Output (2K/4K)

Pro can generate images at 1K (default), 2K, or 4K resolution. Use higher resolutions for:
- Professional assets requiring fine detail
- Large format displays or prints
- Zoom-in-able content

**Note:** Higher resolutions use more tokens (1K: ~1210 tokens, 4K: ~2000 tokens).

### 4. Multi-Image Composition (Up to 14 References)

Combine multiple reference images to create complex compositions:
- Up to **6 high-fidelity object images** to include in the final image
- Up to **5 human images** for character consistency

**Template:**
```
Create [description of final scene] using:
- The [element] from the first image
- The [element] from the second image
- The person from the third image wearing [description]
The final composition should be [style/mood description].
```

### 5. Google Search Grounding

Pro can use Google Search to incorporate real-time data into images.

**Use cases:**
- Current weather visualizations
- Recent events or news-based imagery
- Up-to-date data visualizations (stock charts, statistics)

**Example prompt:**
```
Create an infographic showing the current weather forecast for
San Francisco for the next 5 days.
```

---

## Prompts for Editing Images

These examples show how to provide images alongside your text prompts for editing, composition, and style transfer.

### 1. Adding and Removing Elements

Provide an image and describe your change. The model will match the original image's style, lighting, and perspective.

**Template:**
```
Using the provided image of [subject], please [add/remove/modify] [element]
to/from the scene. Ensure the change is [description of how the change should
integrate].
```

### 2. Inpainting (Semantic Masking)

Conversationally define a "mask" to edit a specific part of an image while leaving the rest untouched.

**Template:**
```
Using the provided image, change only the [specific element] to [new
element/description]. Keep everything else in the image exactly the same,
preserving the original style, lighting, and composition.
```

### 3. Style Transfer

Provide an image and ask the model to recreate its content in a different artistic style.

**Template:**
```
Transform the provided photograph of [subject] into the artistic style of
[artist/art style]. Preserve the original composition but render it with
[description of stylistic elements].
```

### 4. Advanced Composition: Combining Multiple Images

Provide multiple images as context to create a new, composite scene. This is perfect for product mockups or creative collages.

**Template:**
```
Create a new image by combining the elements from the provided images. Take
the [element from image 1] and place it with/on the [element from image 2].
The final image should be a [description of the final scene].
```

### 5. High-Fidelity Detail Preservation

To ensure critical details (like a face or logo) are preserved during an edit, describe them in great detail along with your edit request.

**Template:**
```
Using the provided images, place [element from image 2] onto [element from
image 1]. Ensure that the features of [element from image 1] remain
completely unchanged. The added element should [description of how the
element should integrate].
```

---

## Best Practices

To elevate your results from good to great, incorporate these professional strategies into your workflow.

### Be Hyper-Specific
The more detail you provide, the more control you have. Instead of "fantasy armor," describe it: "ornate elven plate armor, etched with silver leaf patterns, with a high collar and pauldrons shaped like falcon wings."

### Provide Context and Intent
Explain the purpose of the image. The model's understanding of context will influence the final output. For example, "Create a logo for a high-end, minimalist skincare brand" will yield better results than just "Create a logo."

### Iterate and Refine
Don't expect a perfect image on the first try. Use the conversational nature of the model to make small changes. Follow up with prompts like, "That's great, but can you make the lighting a bit warmer?" or "Keep everything the same, but change the character's expression to be more serious."

### Use Step-by-Step Instructions
For complex scenes with many elements, break your prompt into steps. "First, create a background of a serene, misty forest at dawn. Then, in the foreground, add a moss-covered ancient stone altar. Finally, place a single, glowing sword on top of the altar."

### Use "Semantic Negative Prompts"
Instead of saying "no cars," describe the desired scene positively: "an empty, deserted street with no signs of traffic."

### Control the Camera
Use photographic and cinematic language to control the composition. Terms like `wide-angle shot`, `macro shot`, `low-angle perspective`.

---

## Limitations

Be aware of these model constraints:

| Constraint | Flash | Pro |
|------------|-------|-----|
| Max input images | 3 | 14 (6 objects + 5 humans recommended) |
| Output resolution | 1K only | 1K / 2K / 4K |
| Languages | EN, es-MX, fr-FR, de-DE, ja-JP, ko-KR, pt-BR, zh-CN, and more | Same |

**General limitations (both models):**
- No audio or video input support
- Model may not always generate the exact number of images requested
- For best text rendering, generate the text content first, then request the image with that text
- All generated images include a SynthID watermark