clearvars; clc;

% Funzione per leggere il picco massimo memoria su Linux
function peakMB = getMemoryPeakMB_linux()
    peakMB = NaN;
    try
        status = fileread('/proc/self/status');
        expr = 'VmHWM:\s+(\d+) kB';
        tokens = regexp(status, expr, 'tokens');
        if ~isempty(tokens)
            peakKB = str2double(tokens{1}{1});
            peakMB = peakKB / 1024;
        end
    catch
        peakMB = NaN;
    end
end

% Funzione wrapper che chiama la funzione del picco di memoria su windows
function peakMemMB = getPeakMemory()
    if isunix && ~ismac
        % Linux
        peakMemMB = getMemoryPeakMB_linux();
    else
        peakMemMB = NaN;
    end
end

% --- Inizio script principale ---

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

% Preallocazione risultati
matrixNames = strings(1, length(matFiles));
times = zeros(1, length(matFiles));
errors = zeros(1, length(matFiles));
memories_diff = zeros(1, length(matFiles));
memories_peak = zeros(1, length(matFiles));

for k = 1:length(matFiles)

    data = load(matFiles{k}, 'Problem');
    A = sparse(data.Problem.A);

    % Controllo simmetria
    if ~issymmetric(A)
        fprintf('[SKIP] Matrice non simmetrica (%d×%d)\n', size(A,1), size(A,2));
        continue;
    end

    % Pulizia zeri espliciti
    A = spfun(@(x) x, A);

    % Misura memoria prima risoluzione
    vars_before = whos;
    mem_before_vars = sum([vars_before.bytes]) / 1024^2;
    mem_before_sys = getPeakMemory();

    n = size(A,1);
    xe = ones(n,1);
    b = A * xe;

    % Risoluzione sistema
    tic;
    x = A \ b;
    t = toc;

    % Misura memoria dopo risoluzione
    vars_after = whos;
    mem_after_vars = sum([vars_after.bytes]) / 1024^2;
    mem_after_sys = getPeakMemory();

    % Differenza memoria tra dopo e prima (variabili MATLAB)
    mem_used_diff = mem_after_vars - mem_before_vars;

    % Picco massimo memoria (da sistema operativo)
    mem_used_peak = max(mem_before_sys, mem_after_sys);

    % Calcolo errore relativo
    err = norm(x - xe) / norm(xe);

    % Salvataggio risultati
    matrixNames(k) = data.Problem.name;
    times(k) = t;
    errors(k) = err;
    memories_diff(k) = mem_used_diff;
    memories_peak(k) = mem_used_peak;

    clear data A xe b x;
end

set(groot, 'DefaultFigureRenderer', 'painters');

% --- Tabella risultati --- %
T = table(matrixNames.', times.', memories_diff.', memories_peak.', errors.', ...
    'VariableNames', {'Matrix', 'Time_s', 'Memory_Diff_MB', 'Memory_Peak_MB', 'Relative_Error'});

disp('--- Risultati delle simulazioni ---');
disp(T);

% --- Grafici --- %

figure;
semilogy(1:length(matFiles), times, '-o', 'LineWidth', 2, 'Color', [1 0.8 0]);
xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);
ylabel('Tempo (s) - scala log');
xlabel('Matrice');
title('Tempo di risoluzione per ciascuna matrice');
grid on;

% Grafico memoria (modificato per adattarsi al sistema operativo)
figure;
if isunix && ~ismac
    % Linux: mostra sia differenza che picco
    semilogy(1:length(matFiles), memories_diff, '-o', 'LineWidth', 2, 'Color', [1 0.5 0]);
    hold on;
    semilogy(1:length(matFiles), memories_peak, '-o', 'LineWidth', 2, 'Color', [0.7 0.2 0]);
    hold off;
    legend({'Differenza Memoria Variabili MATLAB', 'Picco Memoria OS'}, 'Location', 'best');
else
    % Altri sistemi: mostra solo differenza
    semilogy(1:length(matFiles), memories_diff, '-o', 'LineWidth', 2, 'Color', [1 0.5 0]);
end
xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);
ylabel('Memoria (MB) - scala log');
xlabel('Matrice');
title('Memoria utilizzata');
grid on;

% Grafico errore (rimane invariato)
figure;
semilogy(1:length(matFiles), errors, '-o', 'LineWidth', 2, 'Color', [0 0.6 0]);
xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);
ylabel('Errore relativo - scala log');
xlabel('Matrice');
title('Errore relativo per ciascuna matrice');
grid on;

% Grafico cumulativo (modificato per adattarsi al sistema operativo)
figure;
semilogy(1:length(matFiles), times, '-o', 'LineWidth', 2, 'Color', [1 0.8 0], 'DisplayName', 'Time (s)');
hold on;
semilogy(1:length(matFiles), memories_diff, '-s', 'LineWidth', 2, 'Color', [1 0.5 0], 'DisplayName', 'Memory Diff (MB)');
if isunix && ~ismac
    % Solo su Linux aggiungi il picco
    semilogy(1:length(matFiles), memories_peak, '-d', 'LineWidth', 2, 'Color', [0.7 0.2 0], 'DisplayName', 'Memory Peak (MB)');
end
semilogy(1:length(matFiles), errors, '-^', 'LineWidth', 2, 'Color', [0 0.6 0], 'DisplayName', 'Relative Error');
hold off;

xticks(1:length(matFiles));
xticklabels(matrixNames);
xtickangle(45);
ylabel('Valori (scala log)');
xlabel('Matrice');
title('Confronto cumulativo metriche risoluzione');
legend('Location', 'southeast');
grid on;