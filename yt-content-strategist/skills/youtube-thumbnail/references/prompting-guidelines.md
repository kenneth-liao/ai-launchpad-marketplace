# Prompting Guide and Strategies

Mastering Gemini 2.5 Flash (NanoBanana) Image Generation starts with one fundamental principle:

> **Describe the scene, don't just list keywords.** The model's core strength is its deep language understanding. A narrative, descriptive paragraph will almost always produce a better, more coherent image than a list of disconnected words.

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

Builds on character consistency and scene description to create panels for visual storytelling.

**Template:**
```
A single comic book panel in a [art style] style. In the foreground,
[character description and action]. In the background, [setting details].
The panel has a [dialogue/caption box] with the text "[Text]". The lighting
creates a [mood] mood. [Aspect ratio].
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