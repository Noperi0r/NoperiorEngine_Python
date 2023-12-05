// Vertex Shader
#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal; 
layout (location = 2) in vec3 in_position; // model.py에서 만든 vao에서 in position attribute로 input 전달

out vec2 uv_0; // uv 좌표. fragment에서 사용
out vec3 normal;
out vec3 fragPos;

uniform mat4 m_proj; // 4 by 4 행렬. perspective projection matrix
uniform mat4 m_view; // view matrix
uniform mat4 m_model;



// Entry point 
void main()
{
    uv_0 = in_texcoord_0;
    fragPos = vec3(m_model * vec4(in_position, 1.0)); // fragPos도 world space로 전달.   
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);  // world space에서 light 계산. 따라서 model matrix만 곱해줌 
                                                                        // 그냥 m model만 곱하면 모델이 uniformly scaled하지 않을 때 노말 이상하게 나오므로 연산 더 해줌 
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0); // vertex 포지션 정의. 
    // in position은 resterization 위해 더 필요
    // 
}