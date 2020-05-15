#version 430

#define NUMBER_OF_OBJECTS %%NUMBER_OF_OBJECTS%%

layout (local_size_x=1, local_size_y=1) in;

layout (rgba8, location=0) writeonly uniform image2D out_tex;

uniform vec4 objects[NUMBER_OF_OBJECTS];
uniform vec3 colors[NUMBER_OF_OBJECTS];
uniform vec3 background_color;
uniform mat3 perspective_matrix;
uniform vec3 camera_position;
uniform float zoom_level;
uniform bool show_checkboard;

float solarIntensity(in float dist, in float radius) {
    float c = sqrt(1 - dist/radius);
    return 0.3 + 0.93 * c - 0.23 * c * c;
}

float luminance(in vec3 color) {
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}

bool sphere_hit(in vec3 center, in float radius,
                in vec3 ray_origin, in vec3 ray_direction,
                in float t_min, in float t_max,
                out vec3 point, out float t) {

    vec3 omc = ray_origin - center;
    float b = dot(ray_direction, omc);
    float c = dot(omc, omc) - radius * radius;
    float bsqmc = b * b - c;
    if (bsqmc > 0.0) {
        float root = sqrt(bsqmc);
        float temp = -b - root;
        if (t_min < temp && temp < t_max) {
            t = temp;
            point = ray_origin + t * ray_direction;
            return true;
        }
        temp = -b + root;
        if (t_min < temp && temp < t_max) {
            t = temp;
            point = ray_origin + t * ray_direction;
            return true;
        }
    }
    return false;
}

void main() {

    vec2 max_xy = vec2(16.0, 9.0);
    ivec2 texel_pos = ivec2(gl_GlobalInvocationID.xy);

    ivec2 size = imageSize(out_tex);
    vec3 color = background_color;

    if (show_checkboard)
      if (
          ((texel_pos.x / 80) % 2 == 0 && (texel_pos.y / 80) % 2 == 1) ||
          ((texel_pos.x / 80) % 2 == 1 && (texel_pos.y / 80) % 2 == 0)) {
          color = (vec3(1.0) - background_color) / 2;
      }

    vec2 xy = (texel_pos * 2.0 - size) / size;
    vec3 ray_origin = vec3(xy * max_xy, 0.0);
    vec3 ray_direction = vec3(0.0, 0.0, -1.0);

    float t_min = 0;
    float t_max = 1.0 / 0.0;
    vec3 hit_point;
    float hit_t;
    int hit_anything = -1;
    float closest_so_far = t_max;

    mat3 rotation = mat3(vec3(1, 0, 0), vec3(0, 0, 1), vec3(0, 1, 0));

    for (int i = 0; i < NUMBER_OF_OBJECTS; i++) {
        if (sphere_hit(zoom_level * (perspective_matrix * objects[i].xyz
                                     - camera_position),
                       zoom_level * objects[i].w,
                       ray_origin, ray_direction,
                       t_min, closest_so_far,
                       hit_point, hit_t)) {
            hit_anything = i;
            closest_so_far = hit_t;
        }
    }

    if (hit_anything >= 0) {
        float dist = length(zoom_level * (perspective_matrix * objects[hit_anything].xyz
                            - camera_position).xy - hit_point.xy);
        color = solarIntensity(dist, zoom_level * objects[hit_anything].w)
                * colors[hit_anything];
    }

    imageStore(
        out_tex,
        texel_pos,
        vec4(color, luminance(color))
    );
}
