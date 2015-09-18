#include <stdio.h>
#include <wiringPi.h>

int main() {
	int dustPCS=0;
	float dustValue=0;
	int fd=serialOpen("/dev/ttyAMA0",9600);
	char send[]={0x11,0x01,0x01,0xED};
	char respone[7];
	
		write(fd,send,4);
		read(fd,respone,7);
		if(respone[0]=0x16){
			dustPCS=respone[3]*256*256*256+respone[4]*256*256+respone[5]*256+respone[6];
			dustValue=((float)(dustPCS*3528))/100000;
			printf("%f\n",dustValue);
		} else if (respone[0]=0x06) {
			printf("Hey! I Fail to Receive..\n");
		}
		serialClose(fd);
}

