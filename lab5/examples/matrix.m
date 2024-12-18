A = eye(3);
B = ones(3);
C = A .+ B;
print C;

D = zeros(4);
D[0, 0] = 42;
print D;
print D[2, 2];
