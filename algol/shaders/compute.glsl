#version 430

#define NUMBER_OF_OBJECTS %%NUMBER_OF_OBJECTS%%

layout (local_size_x=16, local_size_y=16) in;

layout (rgba8, location=0) writeonly uniform image2D destTex;

uniform vec4 objects[NUMBER_OF_OBJECTS];
uniform vec3 colors[NUMBER_OF_OBJECTS];
uniform vec3 background_color;

bool inCircle(in vec2 pos, in vec4 circle) {
    vec2 dist = circle.xy - pos;
    return dot(dist, dist) < pow(circle.w, 2.0);
}

float solarIntensity(in float dist, in float radius) {
    float c = sqrt(1 - dist/radius);
    return 0.3 + 0.93 * c - 0.23 * c * c;
}

float brightness(in vec3 color) {
    return sqrt(dot(color * vec3(0.299, 0.587, 0.114), vec3(1.0)));
}

void main() {
    ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);

    int closest = -1;
    for (uint i = 0; i < NUMBER_OF_OBJECTS; i++) {
        if (inCircle(texelPos, objects[i])) {
            if (closest != -1) {
                if (objects[closest].z > objects[i].z) {
                    closest = int(i);
                }
            }
            else {
                closest = int(i);
            }
        }
    }
    vec3 color = background_color;

    if (closest != -1) {
        float r = objects[closest].w;
        float dist = distance(objects[closest].xy, texelPos);
        color = solarIntensity(dist, r) * colors[closest];
    }
    imageStore(
        destTex,
        texelPos,
        vec4(color, 1.0)
    );
}
