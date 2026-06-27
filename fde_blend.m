function [t, y] = fde_blend(alpha, f, T, y0, N, omega)
% FDE_BLEND  Fractional Adams predictor-corrector with predictor-corrector
%            blending, for Caputo FDEs of order alpha in (0,1).
%
%   Solves   C_0 D^alpha y(t) = f(t,y),   y(0)=y0   on [0,T], N steps.
%   Accepted value:  y_{n+1} = (1-omega)*yP + omega*yC
%   omega = 1 recovers the classical corrector.
%
% Works in BOTH MATLAB and Octave (uses elementwise .^ throughout).
%
% Reference: M.D. Amjad Ali, "A Predictor-Corrector Blending Scheme ..."
%
% INPUTS
%   alpha : fractional order in (0,1)
%   f     : function handle f(t,y); MUST accept vector t and vector y,
%           returning a vector (use elementwise ops, e.g. @(t,y) -y)
%   T     : final time
%   y0    : initial value
%   N     : number of uniform steps
%   omega : blending weight (default 1.0 = classical)
%
% OUTPUTS
%   t : (N+1)x1 time grid
%   y : (N+1)x1 numerical solution

  if nargin < 6, omega = 1.0; end
  if alpha <= 0 || alpha >= 1
    error('alpha must be in (0,1).');
  end

  h  = T / N;
  t  = (0:N)' * h;
  cP = h^alpha / gamma(alpha + 1);   % predictor prefactor
  cC = h^alpha / gamma(alpha + 2);   % corrector prefactor

  y = zeros(N+1, 1);
  y(1) = y0;

  for n = 0:N-1
    % --- predictor weights b_j (j=0..n) : (n+1-j)^a - (n-j)^a ----------
    jj = (0:n)';
    b  = (n + 1 - jj).^alpha - (n - jj).^alpha;

    % --- corrector weights a_j (j=0..n+1) -----------------------------
    a = corrector_weights(n, alpha);   % (n+2)x1

    % --- function values at known points t_0..t_n ---------------------
    F = f(t(1:n+1), y(1:n+1));         % (n+1)x1
    F = F(:);

    % --- predictor ----------------------------------------------------
    yP = y0 + cP * (b' * F);

    % --- corrector (uses predictor at t_{n+1}) ------------------------
    fP = f(t(n+2), yP);
    yC = y0 + cC * ( a(1:n+1)' * F + a(n+2) * fP );

    % --- blended accepted value ---------------------------------------
    y(n+2) = (1 - omega) * yP + omega * yC;
  end
end

% ----------------------------------------------------------------------
function a = corrector_weights(n, alpha)
% Standard Diethelm-Ford-Freed product-trapezoidal weights (bracket part).
% a(1) -> j=0 ; a(k+1) -> j=k ; a(n+2) -> j=n+1
  a = zeros(n+2, 1);
  a(1) = n^(alpha+1) - (n - alpha) * (n + 1)^alpha;       % j = 0
  for j = 1:n                                             % 1 <= j <= n
    a(j+1) = (n - j + 2)^(alpha+1) + (n - j)^(alpha+1) ...
             - 2*(n - j + 1)^(alpha+1);
  end
  a(n+2) = 1.0;                                           % j = n+1
end
