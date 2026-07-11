from django.utils.safestring import mark_safe
from django import template

register = template.Library()


@register.simple_tag
def placeholder(
    width, height, text="", responsive=True, bg_color="#f4f4f6", text_color="#a0a0a0"
):
    """
    Generate an SVG Placeholder for Images

    Use in template:
    {% placeholder 800 450 "main banner" %}
    """

    if not text:
        text = f"{width} x {height}"

    font_size = min(max(14, width // 18), 42)

    if responsive:
        # ruff: noqa: F841, E501
        svg = f'''
            <svg width="{width}" height="{height}" 
                xmlns="http://www.w3.org/2000/svg" 
                style="background-color: {bg_color}; display: block; width: 100%; height: auto;" role="img" aria-label="Placeholder: {text}">
            
            <!-- Decorative diagonal lines -->
            <line x1="0" y1="0" x2="100%" y2="100%" stroke="#e0e0e0" stroke-width="2"  opacity="0.5"/>
            <line x1="100%" y1="0" x2="0" y2="100%" stroke="#e0e0e0" stroke-width="2"  opacity="0.5"/>
            
            <!-- A semi-transparent rectangle in the center for better text readability -->
            <rect x="20%" y="35%" width="60%" height="30%" rx="8" fill="white" opacity="0.7"/>
            <!-- Main Text -->
            <text x="50%" y="50%" 
                font-family="system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica 
                Neue', sans-serif" 
                font-size="{font_size}px" 
                font-weight="600"
                fill="{text_color}" 
                text-anchor="middle" 
                dominant-baseline="central">
                {text}
            </text>
            
            <!-- A small information box below -->
            <text x="50%" y="90%" 
                font-family="monospace" 
                font-size="11px" 
                fill="#cccccc" 
                text-anchor="middle">
                {width}px x {height}px
            </text>
        </svg>
        '''
    else:
        svg = f'''
            <svg width="{width}" height="{height}" 
                xmlns="http://www.w3.org/2000/svg" 
                style="background-color: {bg_color}; display: block; width: {width}px; height: {height}px;" role="img" aria-label="Placeholder: {text}">
            
            <!-- Decorative diagonal lines -->
            <line x1="0" y1="0" x2="{width}" y2="{height}" stroke="#e0e0e0" stroke-width="2"  opacity="0.5"/>
            <line x1="{width}" y1="0" x2="0" y2="{height}" stroke="#e0e0e0" stroke-width="2"  opacity="0.5"/>
            
            <!-- A semi-transparent rectangle in the center for better text readability -->
            <rect x="{width * 0.2}" y="{height * 0.35}" width="{width * 0.6}" height="{height * 0.3}" rx="8" fill="white" opacity="0.7"/>
            <!-- Main Text -->
            <text x="50%" y="50%" 
                font-family="system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica 
                Neue', sans-serif" 
                font-size="{font_size}px" 
                font-weight="600"
                fill="{text_color}" 
                text-anchor="middle" 
                dominant-baseline="central">
                {text}
            </text>
            
            <!-- A small information box below -->
            <text x="50%" y="{height - 25}" 
                font-family="monospace" 
                font-size="11px" 
                fill="#cccccc" 
                text-anchor="middle">
                {width}px x {height}px
            </text>
        </svg>
        '''
        # ruff: noqa

    return mark_safe(svg)
