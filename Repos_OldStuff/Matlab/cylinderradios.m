V = 2E-6;
beta = pi/2;
alpha = 2;

x = linspace(0,.0001,.223);
ysolve = solve(y^3 + ((3*x)/(beta*tand(alpha)))*y^2 +3*x^2*y ==(3*V)/(2*pi*beta*tand(alpha)^2));

plot(x,y)