attribute vec3 a_position;
attribute vec3 a_normal;
//## ADD CODE HERE ##

uniform mat4 u_model_matrix;
// uniform mat4 u_projection_view_matrix;
uniform mat4 u_projection_matrix;
uniform mat4 u_view_matrix;

uniform vec4 u_light_position;
uniform vec4 u_light_diffuse;
uniform vec4 u_material_diffuse;

varying vec4 v_color;  //Leave the varying variables alone to begin with

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
	// vec4 v = eyePosition - position;

	position = u_model_matrix * position;
	normal = u_model_matrix * normal;

	vec4 s = u_light_position - position;
	float lambert = max(0.0, dot(normal, s) / (length(normal) * length(s)));

	// vec4 h = s + v;
	// float phong = max(0.0, dot(normal, h) / length(normal) * length(h));

	v_color = lambert * u_light_diffuse * u_material_diffuse;

	// ### --- Change the projection_view_matrix to separate view and projection matrices --- ### 
	position = u_view_matrix * position;
	position = u_projection_matrix * position;
	gl_Position = position;
}