attribute vec3 a_position;
attribute vec3 a_normal;

uniform vec4 u_eye_position;
uniform vec4 u_global_ambient;

// Matrices
uniform mat4 u_model_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

// Light1
uniform vec4 u_light_position_1;
uniform vec4 u_light_color_1;		//used for both Diffuse and Specular

// Light2
uniform vec4 u_light_position_2;
uniform vec4 u_light_color_2;		//used for both Diffuse and Specular

// General lights
uniform vec4 u_material_diffuse;	//used for both Diffuse and Ambient
uniform vec4 u_material_specular;
uniform float u_material_shininess;

varying vec4 v_color;

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	position = u_model_matrix * position;
	normal = u_model_matrix * normal;

	// lights
	vec4 v = u_eye_position - position; //this can be calculated once, not per light

	//calculate the following for each light
	// light1
	vec4 s_1 = u_light_position_1 - position;
	vec4 h_1 = s_1 + v;
	float lambert_1 = max(0.0, dot(normal, s_1) / (length(normal) * length(s_1)));
	float phong_1 = max(0.0, dot(normal, h_1) / length(normal) * length(h_1));

	vec4 diffuse_color_1 = u_light_color_1 * u_material_diffuse * lambert_1;
	vec4 specular_color_1 = u_light_color_1 * u_material_specular * pow(phong_1, u_material_shininess);
	vec4 light_calculated_color_1 = diffuse_color_1 + specular_color_1;

	// light2
	vec4 s_2 = u_light_position_2 - position;
	vec4 h_2 = s_2 + v;
	float lambert_2 = max(0.0, dot(normal, s_2) / (length(normal) * length(s_2)));
	float phong_2 = max(0.0, dot(normal, h_2) / length(normal) * length(h_2));

	vec4 diffuse_color_2 = u_light_color_2 * u_material_diffuse * lambert_2;
	vec4 specular_color_2 = u_light_color_2 * u_material_specular * pow(phong_2, u_material_shininess);
	vec4 light_calculated_color_2 = diffuse_color_2 + specular_color_2;

	v_color = u_global_ambient + u_material_diffuse + light_calculated_color_1 + light_calculated_color_2;

	position = u_view_matrix * position;
	position = u_projection_matrix * position;
	gl_Position = position;
}