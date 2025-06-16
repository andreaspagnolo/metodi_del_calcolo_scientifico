clearvars; clc;

% Lista dei file con le matrici
matFiles = {
    'data/ex15.mat', 
    'data/shallow_water1.mat',
    'data/cfd1.mat', 
    'data/cfd2.mat',
    'data/parabolic_fem.mat', 
    'data/apache2.mat',
    'data/G3_circuit.mat'
};

% Preallocazione
matrixNames = strings(1, length(matFiles));
times = zeros(1, length(matFiles));
errors = zeros(1, length(matFiles));
memories = zeros(1, length(matFiles));

for k = 1:length(matFiles)
    clearvars -except matFiles matrixNames times errors memories k

    data = load(matFiles{k}, 'Problem');
    A = sparse(data.Problem.A);

    % Pulizia zeri espliciti
    A = spfun(@(x) x, A);

    n = size(A,1);
    xe = ones(n,1);
    b = A * xe;

    % Misura memoria prima della risoluzione
    vars_before = whos('A', 'b', 'xe');
    mem_before = sum([vars_before.bytes]) / 1024^2;

    % Risoluzione sistema
    tic;
    x = A \ b;
    t = toc;

    % Misura memoria dopo la risoluzione
    vars_after = whos('A', 'b', 'xe', 'x');
    mem_after = sum([vars_after.bytes]) / 1024^2;

    % Memoria effettiva usata per la soluzione
    mem_used = mem_after - mem_before;

    % Calcolo errore relativo
    err = norm(x - xe) / norm(xe);

    % Salvataggio risultati
    matrixNames(k) = data.Problem.name;
    times(k) = t;
    errors(k) = err;
    memories(k) = mem_used;
end

% --- Tabella risultati --- %
T = table(matrixNames.', times.', memories.', errors.', ...
    'VariableNames', {'Matrix', 'Time_s', 'Memory_MB', 'Relative_Error'});

disp('--- Risultati delle simulazioni ---');
disp(T);

% --- Grafico --- %
figure;
hold on;

semilogy(1:length(matFiles), memories, '-o', 'LineWidth', 2, 'Color', [1 0.5 0]); % memory
semilogy(1:length(matFiles), times, '-o', 'LineWidth', 2, 'Color', [1 0.8 0]);   % time
semilogy(1:length(matFiles), errors, '-o', 'LineWidth', 2, 'Color', [0 0.6 0]);  % error

xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);

ylabel('Valore (scala log)');
title('Prestazioni risoluzione sistemi lineari');
legend({'Memory (MB)', 'Time (s)', 'Relative Error'}, 'Location', 'southwest');
grid on;
