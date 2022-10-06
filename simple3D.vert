attribute vec3 a_position;
attribute vec3 a_normal;
//## ADD CODE HERE ##

uniform vec4 u_eye_position;
uniform vec4 u_global_ambient;

// Matrices
uniform mat4 u_model_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

// Lights
uniform vec4 u_light_position;
uniform vec4 u_light_color;			//used for both Diffuse and Specular
uniform vec4 u_material_diffuse;	//used for both Diffuse and Ambient
uniform vec4 u_material_specular;
uniform float u_material_shininess;

varying vec4 v_color;  //Leave the varying variables alone to begin with

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	position = u_model_matrix * position;
	position = u_view_matrix * position;
	position = u_projection_matrix * position;
	gl_Position = position;

	normal = u_model_matrix * normal;

	// lights
	vec4 v = u_eye_position - position; //this can be calculated once, not per light

	//calculate the following for each light
	vec4 s = u_light_position - position;
	vec4 h = s + v;
	float lambert = max(0.0, dot(normal, s) / (length(normal) * length(s)));
	float phong = max(0.0, dot(normal, h) / length(normal) * length(h));

	vec4 diffuse_color = u_light_color * u_material_diffuse * lambert;
	vec4 specular_color = u_light_color * u_material_specular * pow(phong, u_material_shininess);
	vec4 light_calculated_color = diffuse_color + specular_color;

	v_color = u_global_ambient + u_material_diffuse + light_calculated_color;

}