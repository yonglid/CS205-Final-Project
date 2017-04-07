#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

// global variables
float T_output = 60000;
int resolution = 600;
float timestep = 0.01;
float L = 3.0;
int N = 300;
float spacestep = 0.01; // adjust manually!!!
float v_crit = .13;
float t_in = .1;
float t_out = 2.4;
float t_open = 130.0;
float t_close = 150.0;
float K = .001;
float BCL = 400.0;
float sd = 20.0;

float g(float v, float h) {
	if (v <= v_crit) {
		return((1-h)/t_open);
	}
	else {
		return(-1*h/t_close);
	}
}

// single cell voltage condition
float f(float v, float h) {
	return(h*v*v*(1-v)/t_in - v/t_out);
}

// initial values
float v_init(float x) {
	if (x <= 4*spacestep) {
		return(0.8);
	}
	else if (x >= L-4*spacestep) {
		return(0.8);
	}
	else {
		return(0);
	}
}

float h_init(float x) {
	return(1);
}

// returns h^(m+1)
float update_h(float v, float h) {
	return(g(v,h)*timestep + h);
}

// returns v^(m+1) at spot k on middle parts given time m and spot k
float stdupdate_v(int k, float *V, float *H) {
	return((((V[k+1] - 2*V[k] + V[k-1])*(K/(spacestep*spacestep))) + f(V[k],H[k]))* timestep + V[k]);
}
    
float lupdate_v(float *V, float *H) {
    return((((2*V[1] - 2*V[0])*(K/(spacestep*spacestep))) + f(V[0],H[0]))* timestep + V[0]);
}

float rupdate_v(float *V,float *H) {
    return((((2*V[N-1] - 2*V[N])*(K/(spacestep*spacestep))) + f(V[N],H[N]))* timestep + V[N]);
}
    
// generate random fluctuations (using Central Limit Thm)
int rand_fluc(float BCL, float sd) {
	float x = 0;
	for (int i = 0; i < 25; i++) {
		x += rand();
	}
	x -= 25/2.0;
	x /= sqrt(25/12.0);
    return((int)(sd*x + BCL));
}

// copy one float array to another float array
void copy_arr(float *A, float *B, int n) {
	for (int i = 0; i < n; i ++) {
		A[i] = B[i];
	}
}

int main(int argc, char **argv) {

	printf("Initializing...");

	float L_var = rand_fluc(BCL,sd);
	float R_var = rand_fluc(BCL,sd);

	int T = (int) T_output/timestep;
	int frames = T/resolution;

	if (K*timestep/(spacestep*spacestep) > 0.5) {
		printf("CFL condition not met");
		return(0);
	}

	int m = 0;

	// stores voltage, v, at each location, x, in an array
	// (stores one array per timestamp)
	int width = N+1;
	int height = T_output + 2;

	float V_old[width];
	float V_new[width];

	// array for gate function
	float H_old[width];
	float H_new[width];

	// fill in the 1st array w/ initial voltage
	for (int i = 0; i < width; i++) {
		V_old[i] = v_init(i*spacestep);
	}

	float ary1[width];
	for (int i = 0;i < N; i++) {
		ary1[i] = i*spacestep;
	}

	// initialize H values
	for (int i = 0;i < N; i++) {
		H_old[i] = 1;
	}

	// prepare file for writing
	FILE *f = fopen("fulldatac", "wb");

	printf("Loading frame:");

  	// start timer
  	clock_t begin = clock();

	while (m < T+1) {

		// write to file (frequency depends on resolution)
		if (m % resolution == 0) {
			for (int i = 0; i < width-1; i++) {
			fprintf(f,"%f\t",V_old[i]);
			}
			fprintf(f,"%f\n",V_old[width-1]);
		}	


		// fill in interior grid points
		for (int i = 1; i < N; i++) {
			V_new[i] = stdupdate_v(i,V_old,H_old);
		}

		// fill in left boundary
		V_new[0] = lupdate_v(V_old,H_old);
		// fill in right boundary
		V_new[N] = rupdate_v(V_old,H_old);

		for (int i = 0; i < width; i++) {
			H_new[i] = update_h(V_old[i],H_old[i]);
		}

		if ((int)((m+1)*timestep) == R_var) {
			for (int i = N-4; i < width; i++) {
				V_new[i] = 0.8;
			}
			R_var = rand_fluc(BCL,sd) + R_var;
		}

		// update V, H arrays
		copy_arr(V_old,V_new,width);
		copy_arr(H_old,H_new,width);

		m += 1;
	}

	// end timer
	clock_t end = clock();
	double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
	printf("%f",time_spent);

	fclose(f);
	
	return(0);
}
