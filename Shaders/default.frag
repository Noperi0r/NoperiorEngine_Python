// Fragment Shader
#version 330 core

layout (location = 0) out vec4 fragColor; // define fragment color. fragment 컬러가 fragColor 변수에 의해 변경되게 함.
// frame buffer 위치 지정

in vec2 uv_0;

uniform sampler2D u_texture_0; // sampler2d 자료형이 텍스처임 in glsl

void main()
{
    //vec3 color = vec3(uv_0,0);
    vec3 color = texture(u_texture_0, uv_0).rgb; // color에 texture, uv 대입
    fragColor = vec4(color, 1.0);
}
