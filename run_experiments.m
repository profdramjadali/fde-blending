% run_experiments.m
% Reproduces the tables in:
%   M.D. Amjad Ali, "A Predictor-Corrector Blending Scheme that Improves
%   the Convergence of the Fractional Adams Method for Caputo Equations
%   with Structured Solutions"
%
% Compatible with MATLAB and Octave. Requires fde_blend.m in same folder.
% The blending weight omega is chosen per-alpha by 1-D minimization of the
% finest-mesh error (as described in the paper); the fitted values are near 1.

clear; clc;
Nvec = [64 128 256 512];

fprintf('==========================================================\n');
fprintf(' Problem P1:  y = t^2   (single monomial)\n');
fprintf('==========================================================\n');
for a = [0.3 0.6 0.8]
  f  = @(t,y) 2*t.^(2-a)/gamma(3-a);
  ex = @(t) t.^2;
  w  = find_opt_omega(a, f, 0.0, ex);
  print_block(a, f, 0.0, Nvec, w, ex);
end

fprintf('\n==========================================================\n');
fprintf(' Problem P2:  y = t^5 - t^3   (combined monomials)\n');
fprintf('==========================================================\n');
for a = [0.25 0.50 0.75]
  f  = @(t,y) 120*t.^(5-a)/gamma(6-a) - 6*t.^(3-a)/gamma(4-a);
  ex = @(t) t.^5 - t.^3;
  w  = find_opt_omega(a, f, 0.0, ex);
  print_block(a, f, 0.0, Nvec, w, ex);
end

fprintf('\nDone.\n');

% ----------------------------------------------------------------------
function w = find_opt_omega(a, f, y0, exactfun)
% 1-D search for the error-optimal omega on the finest mesh (N=512).
  N = 512;
  obj = @(w) blend_err(a, f, y0, N, w, exactfun);
  if exist('OCTAVE_VERSION','builtin')
    w = fminbnd(obj, 0.95, 1.0);          % Octave
  else
    w = fminbnd(obj, 0.95, 1.0);          % MATLAB (same call)
  end
end

function e = blend_err(a, f, y0, N, w, exactfun)
  [t, y] = fde_blend(a, f, 1.0, y0, N, w);
  e = max(abs(exactfun(t) - y));
end

function print_block(a, f, y0, Nvec, omega, exactfun)
  fprintf('\n alpha = %.2f   (omega* = %.4f)\n', a, omega);
  fprintf('  %-6s %-13s %-6s %-13s %-6s\n','h','Class.Err','EOC','Blend.Err','EOC');
  ecp = NaN; emp = NaN;
  for k = 1:numel(Nvec)
    N = Nvec(k);
    [t, yc] = fde_blend(a, f, 1.0, y0, N, 1.0);
    [~, ym] = fde_blend(a, f, 1.0, y0, N, omega);
    ex = exactfun(t);
    ec = max(abs(ex - yc));
    em = max(abs(ex - ym));
    if k == 1
      fprintf('  1/%-4d %.3e   %-5s  %.3e   %-5s\n', N, ec, '--', em, '--');
    else
      fprintf('  1/%-4d %.3e   %.2f   %.3e   %.2f\n', N, ec, ...
              log(ecp/ec)/log(2), em, log(emp/em)/log(2));
    end
    ecp = ec; emp = em;
  end
end
