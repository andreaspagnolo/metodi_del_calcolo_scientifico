matrix = load('cfd1.mat');
A = sparse(matrix.Problem.A);

% - Trova gli indici e valori non nulli (inclusi zeri espliciti)
% - Filtra solo i valori diversi da zero
% - Ricrea la matrice
[i,j,s] = find(A);          
mask = s ~= 0;             
A = sparse(i(mask), j(mask), s(mask), size(A,1), size(A,2)); 

disp(matrix.Problem.name); %stampa nome matrice

% Calcolo del numero di condizionamento della matrice.
k = condest(A); 

% Impostazione della soluzione esatta formata solo da 1.
xe = ones(length(A),1);

% Calcolo del vettore dei termini noti a partire dalla matrice A e
% dalla soluzione esatta.
b = A*xe;

% stato prima
m1 = whos; 
tic; %inizia a contare tempo

x = A\b;

%termnina di contare tempo
time = toc; 
% stato dopo
m2 = whos; 

mem1 = sum([m1.bytes]);
mem2 = sum([m2.bytes]);

%calcolo errore relativo
error = norm(x-xe,2)/norm(xe,2); 

disp("relative error: "+ error);
disp("time for cholesnki calcolation: "+time);
disp("memory in MB used for cholesnki calcolation:"+(mem2 - mem1) / 1024^2);