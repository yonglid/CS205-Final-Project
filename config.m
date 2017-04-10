
%FHN eqns:

%dv/dt = -v*(v-a)*(v-1)-w+I0
%dw/dt = eps*(v-d*w)


function FHN
% dimensionless model of excitability
% v=Y(1); w=Y(2);
v0=0.;w0=0;
a=0.1;d=1;eps=0.01;I0=.1;
Y0=[v0,w0];
t=0:0.1:400;
options=odeset('RelTol',1.e-5);
[T, Y]=ode45(@dydt_FHN,t,Y0,options,a,eps,d,I0);
figure(1);clf;
plot(T,Y(:,1),T,Y(:,2)); % time courses of V and w
legend('v(t)','w(t)');
xlabel('Time'); ylabel('v, w');
vpts=(-1.5:.05:1.5);
figure(2);clf;
hold on;
plot(Y(:,1),Y(:,2)); % V-w phase plane 
%determine and plot the v,w-nullclines
%options=optimset; % sets options in fzero to default values
%for k=1:61
%vnullpts(k)=fzero(@vrhs_FHN,[-10 10],options,vpts(k),a,I0);  
%end
vnullpts=-vpts.*(vpts-a).*(vpts-1)+I0;
wnullpts=vpts/d;
plot(vpts,vnullpts,'black',vpts,wnullpts,'black');
xlabel('v'); ylabel('w');
axis([-1 1.5 -.5 1]);

%+++++++++++++++++++

function dY=dydt_FHN(t,Y,a,eps,d,I0)
v=Y(1);
w=Y(2);
dY=zeros(2,1);
dY(1)=-v*(v-a)*(v-1)-w+I0*1/(1+exp(20-t)/.2);
dY(2)=eps*(v-d*w);

%++++++++++++++++++++

function val=vrhs_FHN(w,v,a,I0)
	val=-v*(v-a)*(v-1)-w+I0;
