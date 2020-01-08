/*
 ============================================================================
 Name        : remoteServer.c
 Author      : qqqq
 Version     :
 Copyright   : Your copyright notice
 Description : Hello World in C, Ansi-style
 ============================================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <errno.h>

int castArg(char *str ){

	long val;
	char *endptr;
	errno = 0;

	//metatropi apo string se long
	val = strtol(str, &endptr, 10);

	//elegxos timis
	if ((errno == ERANGE && (val == LONG_MAX || val == LONG_MIN)) || (errno != 0 && val == 0)) {
		puts("value error");
		exit(EXIT_FAILURE);
	}

	//an to string den periexei arithmous
	if (endptr == str) {
		exit(EXIT_FAILURE);
	}

	//elegxos an o arithmos mporei na ginei int
	if (val < INT_MIN || val > INT_MAX){
		puts("cast error");
		exit(EXIT_FAILURE);
	}

	return (int) val;//metatropi apo long se int
}








int main(int argc, char* argv[]) {


	//elegxos arithmou orismaton
	if (argc != 3){  //to onoma tou arxeiou brisketai sti thesi argv[0]
		puts("Incorrect number of arguments");
		return EXIT_FAILURE;
	}

	int portNumber  = castArg(argv[1]);
	int numChildren = castArg(argv[2]);

	if (numChildren < 1){
		puts("incorrect number of Children");
		exit(EXIT_FAILURE);
	}

	printf("portNumber = %d\n", portNumber);
	printf("numChildren = %d\n", numChildren);






	puts("!!!Hello World!!!"); /* prints !!!Hello World!!! */
	return EXIT_SUCCESS;
}
