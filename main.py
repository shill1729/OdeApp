import streamlit as st
import matplotlib.pyplot as plt
from dynamics import *


def ode_analysis(rect,x0,tn):
    dynamics_subs = [expr.subs(dict(zip(st.session_state.params, st.session_state.param_values))) for expr in st.session_state.dynamics]
    ode = DynamicSystem(dynamics_subs, st.session_state.inputs)
    output = ode.stability_analysis()
    st.text(output)
    # rect = [-10, 10, -10, 10]
    fig, ax = plt.subplots(figsize=(8, 8))
    ode.plot_phase_space(rect, 0, 1, ax)
    st.pyplot(fig)
    fig2 = plt.figure(figsize=(8, 8))
    ode.plot_phase_space_trajectory(0, 1, x0,tn)
    st.pyplot(fig2)


def main():
    st.title("Linear stability analysis of ODEs")
    input_str = st.sidebar.text_input("Input variables (comma-separated)", value="x,y")
    param_str = st.sidebar.text_input("Parameters (comma-separated)", value="a,b")
    dyn_str = st.sidebar.text_input("Dynamics (comma-separated)", value="y, a*y-b*x")
    initial_str = st.sidebar.text_input("Initial (comma-separated)", value="0,1")
    tn = st.sidebar.slider("Time-horizon", min_value=0.01, max_value=1000., value=100., step=0.01)
    limits = st.sidebar.text_input("Rectangle (comma-separated)", value = "-10,10,-10,10" )
    limits1 = [float(i.strip()) for i in limits.split(",")]
    params = [sp.Symbol(s.strip()) for s in param_str.split(",")]
    # Create parameter sliders:
    # Create sliders for each parameter
    param_values = []
    init_param = [0.15, 0.25]
    for i, param in enumerate(params):
        param_value = st.sidebar.slider(label=str(param), min_value=-10.0, max_value=10.0, value=init_param[i], step=0.01)
        param_values.append(param_value)
    # Store the current slider values in session state
    st.session_state.param_values = param_values
    inputs = [sp.Symbol(s.strip()) for s in input_str.split(",")]
    dynamics1 = [sp.sympify(s.strip()) for s in dyn_str.split(",")]
    x0 = np.array([float(s.strip()) for s in initial_str.split(",")])
    st.write("Dynamics equations:")
    for i, eq in enumerate(dynamics1):
        st.write(f"{inputs[i]}'(t) = {eq}")
    st.session_state.inputs = inputs
    st.session_state.params = params
    st.session_state.dynamics = dynamics1
    ode_analysis(limits1, x0, tn)


if __name__ == "__main__":
    main()
