clearvars; clc;

Lista dei file con le matrici
matFiles = {
    'data/ex15.mat', 
    'data/shallow_water1.mat', 
    'data/cfd1.mat', 
    'data/cfd2.mat',
    'data/parabolic_fem.mat', 
    'data/apache2.mat', 
    'data/G3_circuit.mat',
    'data/Flan_1565.mat',
    'data/StocF-1465.mat'
};

matFiles = {};

% Preallocazione
matrixNames = strings(1, length(matFiles));
times = zeros(1, length(matFiles));
errors = zeros(1, length(matFiles));
memories = zeros(1, length(matFiles));

% Ciclo sulle matrici
for k = 1:length(matFiles)
    data = load(matFiles{k}, 'Problem');
    A = sparse(data.Problem.A);

    % Pulizia zeri espliciti
    A = spfun(@(x) x, A);

    n = size(A,1);
    xe = ones(n,1);
    b = A * xe;

    m1 = whos;
    tic;
    x = A \ b;
    t = toc;
    m2 = whos;

    err = norm(x - xe) / norm(xe);
    mem = (sum([m2.bytes]) - sum([m1.bytes])) / 1024^2;

    % Salvataggio risultati
    matrixNames(k) = data.Problem.name;
    times(k) = t;
    errors(k) = err;
    memories(k) = mem;
end

T = table(matrixNames.', times.', memories.', errors.', ...
    'VariableNames', {'Matrix', 'Time_s', 'Memory_MB', 'Relative_Error'});

disp('--- Risultati delle simulazioni ---');
disp(T);

% --- Grafico unico ---
figure;
hold on;

% Plot (usa loglog per entrambe le scale log, oppure semilogy per solo Y log)
semilogy(1:length(matFiles), memories, '-o', 'LineWidth', 2, 'Color', [1 0.5 0]); % chol_size
semilogy(1:length(matFiles), times, '-o', 'LineWidth', 2, 'Color', [1 0.8 0]);   % total_time
semilogy(1:length(matFiles), errors, '-o', 'LineWidth', 2, 'Color', [0 0.6 0]);  % err

% Etichette e leggenda
xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);

ylabel('Valore (scala log)');
title('Prestazioni risoluzione sistemi lineari');
legend({'chol\_size (MB)', 'total\_time (s)', 'err'}, 'Location', 'southwest');
grid on;