#version 330
in vec2 TexCoords;
out vec4 outColor;
uniform sampler2D texture1;
void main()
{
    outColor = texture(texture1, TexCoords);
}