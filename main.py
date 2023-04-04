import streamlit as st
import matplotlib.pyplot as plt
from dynamics import *


def ode_analysis(rect):
    dynamics_subs = [expr.subs(dict(zip(st.session_state.params, st.session_state.param_values))) for expr in st.session_state.dynamics]
    ode = DynamicSystem(dynamics_subs, st.session_state.inputs)
    output = ode.stability_analysis()
    st.text(output)
    # rect = [-10, 10, -10, 10]
    fig, ax = plt.subplots(figsize=(8, 8))
    ode.plot_phase_space(rect, 0, 1, ax)
    st.pyplot(fig)


def main():
    st.title("Linear stability analysis of ODEs")
    input_str = st.sidebar.text_input("Input variables (comma-separated)", value="x,y")
    param_str = st.sidebar.text_input("Parameters (comma-separated)", value="a,b,c,d")
    dyn_str = st.sidebar.text_input("Dynamics (comma-separated)", value="a*x + b*y, c*x+d*y")
    limits = st.sidebar.text_input("Rectangle (comma-separated)", value = "-10,10,-10,10" )
    limits1 = [float(i.strip()) for i in limits.split(",")]
    params = [sp.Symbol(s.strip()) for s in param_str.split(",")]
    # Create parameter sliders:
    # Create sliders for each parameter
    param_values = []
    init_param = [4.0, 3.0, 2., 1.]
    for i, param in enumerate(params):
        param_value = st.sidebar.slider(label=str(param), min_value=-10.0, max_value=10.0, value=init_param[i], step=0.01)
        param_values.append(param_value)
    # Store the current slider values in session state
    st.session_state.param_values = param_values
    inputs = [sp.Symbol(s.strip()) for s in input_str.split(",")]
    dynamics1 = [sp.sympify(s.strip()) for s in dyn_str.split(",")]
    st.write("Dynamics equations:")
    for i, eq in enumerate(dynamics1):
        st.write(f"{inputs[i]}'(t) = {eq}")
    st.session_state.inputs = inputs
    st.session_state.params = params
    st.session_state.dynamics = dynamics1
    ode_analysis(limits1)


if __name__ == "__main__":
    main()
