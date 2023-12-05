// Fragment Shader
#version 330 core

layout (location = 0) out vec4 fragColor; // define fragment color. fragment 컬러가 fragColor 변수에 의해 변경되게 함.
// frame buffer 위치 지정

in vec2 uv_0;  
in vec3 normal; // vert에서부터 input 가져옴
in vec3 fragPos;

struct Light
{
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0; // sampler2d 자료형이 텍스처임 in glsl
uniform vec3 camPos;

vec3 getLight(vec3 color)
{
    vec3 Normal = normalize(normal);

    // ambient light
    vec3 ambient = light.Ia;

    // diffuse light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    // specular light 
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    return color * (ambient + diffuse + specular);
} 

void main()
{
    //vec3 color = vec3(uv_0,0);
    vec3 color = texture(u_texture_0, uv_0).rgb; // color에 texture, uv 대입
    color = getLight(color);
    fragColor = vec4(color, 1.0);
}
