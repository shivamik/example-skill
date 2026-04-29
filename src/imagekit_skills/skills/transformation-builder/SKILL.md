---
name: transformation-builder
description: >
  Build ImageKit image and video transformation URLs from natural language
  descriptions. Use when the user wants to resize, crop, overlay, format,
  optimize, or apply any visual transformation to images or videos using
  ImageKit. Also use when the user provides an ImageKit URL and wants to
  modify its transformations.
---

# ImageKit Transformation Builder

When the user wants to transform an image or video:

1. Use the `transformation_builder` MCP tool
2. Pass the user's natural language description of the desired transformation
3. Return the generated transformation URL or parameters
4. Explain what each transformation parameter does

## When to Use

- User wants to resize, crop, or reformat an image
- User wants to add overlays, watermarks, or text
- User wants to optimize images for web performance
- User wants to apply effects (blur, grayscale, contrast, etc.)
- User provides an ImageKit URL and wants modifications
- User asks to generate a transformation URL

## Example Requests

- "Resize this image to 400x300 with smart crop"
- "Add a watermark in the bottom-right corner"
- "Convert this to WebP with 80% quality"
- "Create a 200x200 thumbnail with face detection"
- "Apply a blur effect with radius 10"

## Tips

- Ask for the source image URL if not provided
- Suggest optimization parameters (format auto, quality auto) when appropriate
- Explain the transformation chain so users can modify it later
- For complex transformations, break them down step by step
