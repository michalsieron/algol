#version 330

#define NUMBER_OF_OBJECTS %%NUMBER_OF_OBJECTS%%

uniform float radii[NUMBER_OF_OBJECTS];
uniform vec3 colors[NUMBER_OF_OBJECTS];
uniform vec2 window_size;

in vec3 in_position;
out vec3 color;

void main() {
    gl_Position = vec4(in_position, 1.0);
    gl_PointSize = radii[gl_VertexID];
    color = colors[gl_VertexID];
}
