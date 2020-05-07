#version 330

in vec3 color;
out vec4 out_color;

void main() {
    float dist = step(length(gl_PointCoord.xy - vec2(0.5)), 0.5);
    out_color = vec4(dist * color, dist);
}
