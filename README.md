# OdeApp
This is a streamlit app, [OdeApp](https://shill1729-odeapp-main-54kuic.streamlit.app/) for performing
stability analysis on a dynamical system specified by a system of ODEs, using linearization.

We present an implementation of basic linearization and stability analysis of dynamical systems in the SymPy package.

We will appeal to authority and reference Strogatz's *Nonlinear Dynamics and Chaos*.

Suppose we have a system
$$x'(t) = f(x(t), y(t))$$
$$y'(t) = g(x(t), y(t))$$
and let $x^\*, y^\*$ be a fixed point of this system i.e. 
$$f(x^*, y^*) = 0 \text{ and } g(x^*, y^*) = 0.$$
Perturb the equation by these, and look at the system in $u = x-x^*$ and $v=y-y^*$. Then the system $[x,y]^T$ with dynamics $F=[f, g]^T$ has linearization $w=[u,v]$ with dynamics $G = J_F(z^*) [u,v]^T$ where $J_F(z)$ is the Jacobian matrix of $F$ evaluated at $z=[x,y]$.

The important part is that *as long as the fixed point for the linearized system is not one of the borderline cases below*, this lineariation scheme can classify the dynamical system's stability.

That is, if the linearized system predicts a
- saddle
- node,
- or spiral,

then the fixed point of the original system is really one of those. A proof is in Andronov et al. (1973). The borderline cases are centers, degenerate nodes, stars, or non-isolated fixed points. These are more delicate.

The classification of a linear system $x'(t) = AF(x)$ with matrix $A$ can be given as follows. Let $\tau$ be the trace of $A$ and $\Delta$ be the determinant. For a two-dimensional system, we have $\tau = \lambda_1+\lambda_2$ and $\Delta = \lambda_1\lambda_2$, where $\lambda_i$ are the eigenvalues of $A$. The classification scheme is as follows:

### Classification of fixed points:
1. If $\Delta < 0$, we have a saddle point.
2. If $\Delta >0$ we either have nodes ($\lambda_i$ real and same sign) or spirals and centers ($\lambda_i$ complex conjugates of one another)
2. Nodes satisfy $\tau-4\Delta >0$ and spirals satisfy $\tau^2-4\Delta < 0$. The parabola $\tau^2-4\Delta =0$ is teh borderline between nodes and spirals; star nodes and degenerate nodes live on this parabola.
3. If $\Delta = 0$, at least one of the eigenvalues is zero. Then the origin is not an isolated fixed point. There is either a whole line of fixed points, like $y=x$, or a plane of fixed points if $A=0$.

### Stability analysis:
If $\tau < 0$ both eigenvalues have negative real parts, so the fixed point is stable. 
Unstable spirals and nodes have $\tau >0$. 
Neurtrally stable centers live on the 
borderline $\tau=0$, where the eigenvalues are 
purely imaginary.

# Limitations:
Currently, if no analytic solution is possible for the fixed points,
an error is thrown. In the future, I will replace this with a numerical solver.

Also, currently, any parameters you pick are limited to the range $[-10, 10]$, in the future
I will also add optionality to change these regions.

Lastly, greek letters for either the state variables or the
parameters are currently breaking the app. Eventually I will sort this out, as
scientists and mathematicians love this alphabet.



