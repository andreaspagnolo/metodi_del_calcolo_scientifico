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

    data = load(matFiles{k}, 'Problem');
    A = sparse(data.Problem.A);

    %controllo simmetria
    if ~issymmetric(A)
        fprintf('[SKIP] Matrice non simmetrica (%d×%d)\n', size(A,1), size(A,2));
        continue;
    end

    % Pulizia zeri espliciti
    A = spfun(@(x) x, A);

    % Misura memoria prima della risoluzione
    vars_before = whos;
    mem_before = sum([vars_before.bytes]) / 1024^2;

    n = size(A,1);
    xe = ones(n,1);
    b = A * xe;

    % Risoluzione sistema
    tic;
    x = A \ b;
    t = toc;

    % Misura memoria dopo la risoluzione
    vars_after = whos;
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

    clear data A xe b x;
end

% --- Tabella risultati --- %
T = table(matrixNames.', times.', memories.', errors.', ...
    'VariableNames', {'Matrix', 'Time_s', 'Memory_MB', 'Relative_Error'});

disp('--- Risultati delle simulazioni ---');
disp(T);

% --- Grafico Tempo --- %
figure;
plot(1:length(matFiles), times, '-o', 'LineWidth', 2, 'Color', [1 0.8 0]);
xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);
ylabel('Tempo (s)');
xlabel('Matrice');
title('Tempo di risoluzione per ciascuna matrice');
grid on;

% --- Grafico Memoria --- %
figure;
plot(1:length(matFiles), memories, '-o', 'LineWidth', 2, 'Color', [1 0.5 0]);
xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);
ylabel('Memoria utilizzata (MB)');
xlabel('Matrice');
title('Memoria utilizzata per ciascuna matrice');
grid on;

% --- Grafico Errore --- %
figure;
plot(1:length(matFiles), errors, '-o', 'LineWidth', 2, 'Color', [0 0.6 0]);
xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);
ylabel('Errore relativo');
xlabel('Matrice');
title('Errore relativo per ciascuna matrice');
grid on;

% --- Grafico complessivo --- %
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
legend({'Memory (MB)', 'Time (s)', 'Relative Error'}, 'Location', 'northwest');
grid on;