attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec4 a_eye_position;

uniform mat4 u_model_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

uniform vec4 u_global_ambient;

uniform vec4 u_light_1_position;
uniform vec4 u_light_1_diffuse;
uniform vec4 u_light_1_specular;
uniform vec4 u_light_1_ambient;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform vec4 u_material_ambient;
uniform vec4 u_material_emission;
uniform float u_material_shininess;

varying vec4 v_color;

void main(void)
{
	vec4 v = a_eye_position - a_position; //this can be calculated once, not per light
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	//calculate the following for each light
	vec4 s_1 = u_light_1_position - position;
	vec4 h_1 = s + v;

	float lambert_1 = max(0.0, dot(normal, s_1) / (length(normal) * length(s)));
	float phong_1 = max(0.0, dot(normal, h_1) / length(normal) * length(h));

	vec4 ambient_color_1 = u_light_1_ambient * u_material_ambient; 
	vec4 diffuse_color_1 = u_light_1_diffuse * u_material_diffuse * lambert_1; 
	vec4 specular_color_1 = u_light_1_specular * u_material_specular * pow(phong_1, u_material_shininess); 
	vec4 light_1_calculated_color = ambient_color_1 + diffuse_color_1 + specular_color_1;
	//imagine we also calculate light2CalculatedColor & light3CalculatedColor, etc.

	v_color = u_global_ambient * u_material_ambient + u_material_emission + light_1_calculated_color; 
			// + light2CalculatedColor + light3CalculatedColor + ... etc.

	position = u_model_matrix * position;
	normal = u_model_matrix * normal;

	position = u_view_matrix * position;
	position = u_projection_matrix * position;
	gl_Position = position;
}