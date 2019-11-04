uniform sampler2D u_tex01;	// texture 1
uniform sampler2D u_tex02;	// Texture 2 (alphatexture)
uniform float u_using_alpha_texture;
uniform float u_opacity;

varying vec2 v_uv;

void main(void)
{
	vec4 color = texture2D(u_tex01, v_uv);
	float opacity = u_opacity;
	// If we are useing a second alpha texture we add it to the opacity
	if (u_using_alpha_texture == 1.0) {
		opacity *= texture2D(u_tex02, v_uv).r;
	}
	// discard opacity that is less than 10%
	if(opacity < 0.1){
		discard;
	}
	
	// set the fragment color
	gl_FragColor = color;
	// set the fragment obacity
	gl_FragColor.a = opacity;
}