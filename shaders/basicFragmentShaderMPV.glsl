#version 330 core

in vec2 outTexCoords;

out vec4 color;
uniform sampler2D samplerTex;

void main()
{
	color = texture( samplerTex, outTexCoords );
}
