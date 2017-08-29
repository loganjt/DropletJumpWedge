clear all 
clc

V = 2000;
beta = pi/2;
tan_alpha = tand(2);


a1 = (V)/(2*pi*tan_alpha);
a2 = beta*tan_alpha;
a3 = 1;
a4 = 0.33*beta*tan_alpha;

r3 = ones(1,152);
for x = 71:223
    syms y
    y_solved = vpasolve(a4*y^3 + a3*x*y^2 + a2*x^2*y == a1, y,[0,250]);
    r3(x-70) = y_solved;
end

x = 71:223;
y_approx = (.5*beta*tan_alpha*x).*(sqrt(1+((2*V)./(beta^2*pi*tan_alpha^3*x.^3)))-1);

plot(x,r3,'o',x,y_approx,'--')
xlabel('x distance from wedge vertex (mm)')
ylabel('inner cylinder radius as f(x) (mm)')
legend('Exact Solution', 'Approximated Solution')
grid on









