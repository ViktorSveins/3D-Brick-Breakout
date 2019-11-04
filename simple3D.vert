attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_uv;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_eye_position;
uniform vec4 u_light_position;

uniform vec4 u_spotlight_position;
varying vec4 v_h_spotlight;
varying vec4 v_s_spotlight;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);
	
	// UV coords sent into per-pixel use
	v_uv = a_uv;

	// local coords
	position = u_model_matrix * position;
	v_normal = normalize(u_model_matrix * normal);
	
	// global coords
	vec4 v = normalize(u_eye_position - position);
    v_s = normalize(u_light_position - position);
	v_h = normalize(v_s + v);

	// Get spotlight s and h vectors (normalized)
	v_s_spotlight = normalize(u_spotlight_position - position);
	v_h_spotlight = normalize(v_s_spotlight + v);
	// eye coords
	position = u_view_matrix * position;

	// clip coords
	position = u_projection_matrix * position;

	gl_Position = position;
}