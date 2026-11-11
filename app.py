import os
import tempfile
from benchmark import benchmark_python_file
import ast
import pandas as pd
import streamlit as st
import os
import tempfile
from benchmark import benchmark_python_file
import ast
import pandas as pd
import streamlit as st

from industrial.combined_report import generate_combined_report
from industrial.carbon_reduction import calculate_process_carbon_reduction
from industrial.process_analyzer import analyze_process_energy
from comparison import run_comparison
from industrial.sustainability_simulation import simulate_process_improvements
from industrial.process_recommendations import generate_process_recommendations
from energy_test import measure_energy
from comparison import run_comparison
from energy_test import measure_energy
from industrial.factory_calculator import calculate_factory_energy
from industrial.carbon_calculator import calculate_carbon_emissions
from industrial.optimization import simulate_improvement

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="GreenCode Analyzer",
    layout="wide"
)


# ==========================================
# STATIC CODE ANALYZER
# ==========================================

class CodeAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.for_loops = 0
        self.while_loops = 0
        self.nested_loops = 0
        self.loop_depth = 0
        self.membership_checks = []

    def visit_For(self, node):

        self.for_loops += 1

        if self.loop_depth > 0:
            self.nested_loops += 1

        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node):

        self.while_loops += 1

        if self.loop_depth > 0:
            self.nested_loops += 1

        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_Compare(self, node):

        if self.loop_depth > 0:

            if any(
                isinstance(operation, ast.In)
                for operation in node.ops
            ):
                self.membership_checks.append(node.lineno)

        self.generic_visit(node)



# ==========================================
# DASHBOARD HEADER
# ==========================================

st.title("GreenCode Analyzer")

st.subheader(
    "Energy Efficiency and Carbon Emission Analysis"
)

st.write(
    "Analyze Python code, identify potential optimization "
    "opportunities and estimate energy consumption and "
    "carbon emissions."
)

st.divider()


# ==========================================
# MODULE 1: PYTHON FILE UPLOAD
# ==========================================

st.header("1. Static Code Analysis")

uploaded_file = st.file_uploader(
    "Upload a Python file",
    type=["py"]
)

if uploaded_file is not None:

    st.success(f"File uploaded: {uploaded_file.name}")

    try:
        source_code = uploaded_file.getvalue().decode("utf-8")

        with st.expander("View uploaded Python code"):
            st.code(source_code, language="python")

        if st.button("Analyze Code", type="primary"):

            try:
                syntax_tree = ast.parse(source_code)

                analyzer = CodeAnalyzer()
                analyzer.visit(syntax_tree)

                st.session_state.analysis_results = {
                    "for_loops": analyzer.for_loops,
                    "while_loops": analyzer.while_loops,
                    "nested_loops": analyzer.nested_loops,
                    "membership_checks": analyzer.membership_checks
                }

                st.success("Static analysis completed!")

            except SyntaxError as error:

                st.session_state.pop("analysis_results", None)

                st.error(
                    f"Syntax error on line {error.lineno}: "
                    f"{error.msg}"
                )

    except UnicodeDecodeError:

        st.error(
            "Unable to read this file as UTF-8 text."
        )


# ==========================================
# DISPLAY STATIC ANALYSIS RESULTS
# ==========================================
st.divider()
st.header("2. Performance Benchmark")

st.write(
    "Measure the execution time, CPU usage and "
    "peak memory of your uploaded Python file."
)

if uploaded_file is None:
    st.info("Please upload a Python file to run the performance benchmark.")

else:
    if st.button("Run Performance Benchmark", type="primary"):
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                suffix=".py",
                delete=False
            ) as temp_file:

                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            with st.spinner("Running performance benchmark..."):
                results = benchmark_python_file(temp_path)

            st.session_state.performance_results = results

        except Exception as error:
            st.error(f"Benchmark failed: {error}")

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

performance = st.session_state.get("performance_results")

if performance is not None:

    st.subheader("Performance Results")

    col1, col2 = st.columns(2)

    col1.metric(
        "Execution Time",
        f"{performance['execution_time']:.4f} seconds"
    )

    col2.metric(
        "CPU Time",
        f"{performance['cpu_time']:.4f} seconds"
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "CPU Usage",
        f"{performance['cpu_usage']:.2f}%"
    )

    col4.metric(
        "Peak Memory",
        f"{performance['peak_memory']:.2f} MB"
    )

    if performance["timed_out"]:
        st.warning("Program stopped because the time limit was reached.")

    elif performance["return_code"] == 0:
        st.success("Performance benchmark completed successfully.")

    else:
        st.error("The uploaded program ended with an error.")

        if performance["error_message"]:
            st.code(performance["error_message"])

    st.caption(
        "CPU and memory values are process-level estimates. "
        "Short programs may produce less accurate measurements."
    )

# =====
    # ==========================================
    # PERFORMANCE ANALYSIS & SUGGESTIONS
    # ==========================================

    st.divider()
    st.subheader("Performance Analysis")
    
    st.write(
        "Based on the measured performance, "
        "here are some observations and suggestions."
    )

    suggestions_found = False

    if performance["timed_out"]:
        st.warning(
            "Execution Time: The program exceeded the time limit. "
            "Review loops, recursion and repeated computations."
        )
        suggestions_found = True

    else:

        if performance["execution_time"] > 2:
            st.warning(
                "Execution Time: The program took more than 2 seconds. "
                "Review algorithm complexity and unnecessary operations."
            )
            suggestions_found = True

        if performance["cpu_usage"] > 80:
            st.warning(
                "CPU Usage: High CPU activity was observed. "
                "Check for unnecessary calculations or repeated processing."
            )
            suggestions_found = True

        if performance["peak_memory"] > 100:
            st.warning(
                "Memory Usage: The program used more than 100 MB of memory. "
                "Review large data structures and unnecessary copies."
            )
            suggestions_found = True

    if not suggestions_found:
        st.success(
            "No performance warning was triggered by the current rules."
        )

    st.caption(
        "These are heuristic suggestions, not proof of inefficient code. "
        "Thresholds are illustrative and may need adjustment for different systems."
    )
    
# ==========================================
# SMART CODE OPTIMIZATION EXAMPLES
# ==========================================

st.divider()
st.header("Smart Code Optimization Examples")

analysis_data = st.session_state.get("analysis_results")

if analysis_data is None:
    st.info("Run Static Code Analysis first to see optimization examples.")

else:
    examples_found = False

    # Example 1: Membership Check Optimization
    if analysis_data["membership_checks"]:

        examples_found = True

        st.subheader("1. Optimize Membership Checking")

        st.write(
            "Your code contains membership checks inside loops. "
            "If the searched collection is a list and repeated "
            "lookups are needed, a set may improve lookup performance."
        )

        with st.expander("View original and optimized examples"):

            st.write("Original approach:")

            st.code(
                """
registered_students = ["Aman", "Riya", "Rahul"]

for student in students:
    if student in registered_students:
        print(student)
                """,
                language="python"
            )

            st.write("Possible optimized approach:")

            st.code(
                """
registered_students = ["Aman", "Riya", "Rahul"]

registered_set = set(registered_students)

for student in students:
    if student in registered_set:
        print(student)
                """,
                language="python"
            )

            st.caption(
                "Set membership has average O(1) lookup time, "
                "compared with O(n) for a list. Creating the set "
                "also takes time and memory, so it is most useful "
                "for repeated lookups."
            )

    # Example 2: Nested Loop Optimization
    if analysis_data["nested_loops"] > 0:

        examples_found = True

        st.subheader("2. Review Nested Loop Optimization")

        st.write(
            "Nested loops were detected. In some problems, "
            "a dictionary or set can avoid repeated searching."
        )

        with st.expander("View an illustrative example"):

            st.write("Original approach:")

            st.code(
                """
for student in students:
    for registered in registered_students:
        if student == registered:
            print(student)
                """,
                language="python"
            )

            st.write("Possible optimized approach:")

            st.code(
                """
registered_set = set(registered_students)

for student in students:
    if student in registered_set:
        print(student)
                """,
                language="python"
            )

            st.caption(
                "This transformation is suitable for membership "
                "matching. It is not a universal replacement for "
                "all nested loops."
            )

    if not examples_found:
        st.success(
            "No optimization example is available for the "
            "patterns detected in this code."
        )

# MODULE 2: ENERGY AND CARBON MONITORING
# ==========================================

st.divider()

st.header("2. Energy and Carbon Monitoring")

st.write(
    "Run a controlled computational workload to estimate "
    "energy consumption and carbon emissions."
)

if st.button("Start Energy Monitoring", type="primary"):

    with st.spinner(
        "Measuring energy consumption and CO2 emissions..."
    ):

        try:

            energy_results = measure_energy()

            st.session_state.energy_results = energy_results

        except Exception as error:

            st.error(f"Energy monitoring failed: {error}")


energy = st.session_state.get("energy_results")

if energy is not None:

    st.success("Energy monitoring completed!")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Execution Time",
        f"{energy['duration']:.2f} seconds"
    )

    col2.metric(
        "Energy Consumption",
        f"{energy['energy']:.8f} kWh"
    )

    col3.metric(
        "CO2 Emissions",
        f"{energy['co2']:.8f} kg CO2e"
    )

    col4, col5 = st.columns(2)

    col4.metric(
        "CPU Energy",
        f"{energy['cpu_energy']:.8f} kWh"
    )

    col5.metric(
        "RAM Energy",
        f"{energy['ram_energy']:.8f} kWh"
    )

    st.caption(
        "Values are estimates generated by CodeCarbon, "
        "not direct electricity-meter measurements."
    )


# ==========================================
# MODULE 3: ORIGINAL VS OPTIMIZED COMPARISON
# ==========================================

st.divider()

st.header("3. Original vs Optimized Code Comparison")

st.write(
    "Compare two algorithms solving the same problem "
    "and observe their execution time, energy consumption "
    "and estimated carbon emissions."
)

if st.button("Run Code Comparison", type="primary"):

    with st.spinner(
        "Running original and optimized algorithms..."
    ):

        try:

            comparison_results = run_comparison()

            st.session_state.comparison_results = comparison_results

        except Exception as error:

            st.error(f"Comparison failed: {error}")


comparison = st.session_state.get("comparison_results")

if comparison is not None:

    original = comparison["original"]
    optimized = comparison["optimized"]

    st.success("Comparison completed successfully!")

    # Execution time

    st.subheader("Execution Time")

    col1, col2 = st.columns(2)

    col1.metric(
        "Original Approach",
        f"{original['time']:.4f} seconds"
    )

    col2.metric(
        "Optimized Approach",
        f"{optimized['time']:.4f} seconds"
    )

    st.bar_chart(
        pd.DataFrame({
            "Execution Time (seconds)": [
                original["time"],
                optimized["time"]
            ]
        }, index=["Original", "Optimized"])
    )

    # Energy comparison

    st.subheader("Energy Consumption")

    col3, col4 = st.columns(2)

    col3.metric(
        "Original Energy",
        f"{original['energy']:.8f} kWh"
    )

    col4.metric(
        "Optimized Energy",
        f"{optimized['energy']:.8f} kWh"
    )

    st.bar_chart(
        pd.DataFrame({
            "Energy (kWh)": [
                original["energy"],
                optimized["energy"]
            ]
        }, index=["Original", "Optimized"])
    )

    # CO2 comparison

    st.subheader("CO2 Emissions")

    col5, col6 = st.columns(2)

    col5.metric(
        "Original CO2",
        f"{original['emissions']:.8f} kg CO2e"
    )

    col6.metric(
        "Optimized CO2",
        f"{optimized['emissions']:.8f} kg CO2e"
    )

    st.bar_chart(
        pd.DataFrame({
            "CO2 (kg CO2e)": [
                original["emissions"],
                optimized["emissions"]
            ]
        }, index=["Original", "Optimized"])
    )

    # Verify results

    st.subheader("Optimization Results")

    if comparison["results_match"]:

        st.success(
            "Both approaches produced the same result."
        )

    else:

        st.error(
            "The results do not match. Optimization needs review."
        )

    # Reduction metrics

    if comparison["energy_reduction"] is not None:

        st.metric(
            "Estimated Energy Reduction",
            f"{comparison['energy_reduction']:.2f}%"
        )

    else:

        st.info(
            "Energy reduction cannot be calculated."
        )

    if comparison["emission_reduction"] is not None:

        st.metric(
            "Estimated CO2 Reduction",
            f"{comparison['emission_reduction']:.2f}%"
        )

    else:

        st.info(
            "CO2 reduction cannot be calculated."
        )

    st.caption(
        "Energy and CO2 values are CodeCarbon estimates. "
        "Small workloads can produce noisy measurements. "
        "Repeat experiments before drawing conclusions."
    )

    # ==========================================
    # MODULE 4: DOWNLOAD COMPARISON REPORT
    # ==========================================

    st.divider()

    st.subheader("4. Download Comparison Report")

    report_data = pd.DataFrame([
        {
            "Metric": "Execution Time",
            "Original": original["time"],
            "Optimized": optimized["time"],
            "Unit": "seconds"
        },
        {
            "Metric": "Energy Consumption",
            "Original": original["energy"],
            "Optimized": optimized["energy"],
            "Unit": "kWh"
        },
        {
            "Metric": "CO2 Emissions",
            "Original": original["emissions"],
            "Optimized": optimized["emissions"],
            "Unit": "kg CO2e"
        }
    ])

    csv_report = report_data.to_csv(index=False)

    st.download_button(
        label="Download CSV Report",
        data=csv_report,
        file_name="GreenCode_Comparison_Report.csv",
        mime="text/csv"
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "GreenCode Analyzer | Energy Efficiency | "
    "Carbon Emission Estimation | Code Optimization"
)

# ==========================================
# COMPLETE GREEN SOFTWARE ANALYSIS REPORT
# ==========================================

st.divider()

st.header("5. Complete Green Software Analysis Report")

st.write(
    "Generate a combined report containing static analysis, "
    "energy monitoring and algorithm comparison results."
)

if (
    "analysis_results" in st.session_state
    and "energy_results" in st.session_state
    and "comparison_results" in st.session_state
):

    if st.button("Generate Complete Report", type="primary"):

        analysis = st.session_state.analysis_results
        energy = st.session_state.energy_results
        comparison = st.session_state.comparison_results

        original = comparison["original"]
        optimized = comparison["optimized"]

        complete_report = pd.DataFrame([
            {
                "Category": "Static Analysis",
                "Metric": "For Loops",
                "Value": analysis["for_loops"],
                "Unit": "count"
            },
            {
                "Category": "Static Analysis",
                "Metric": "While Loops",
                "Value": analysis["while_loops"],
                "Unit": "count"
            },
            {
                "Category": "Static Analysis",
                "Metric": "Nested Loops",
                "Value": analysis["nested_loops"],
                "Unit": "count"
            },
            {
                "Category": "Static Analysis",
                "Metric": "Membership Checks",
                "Value": len(analysis["membership_checks"]),
                "Unit": "count"
            },
            {
                "Category": "Energy Monitoring",
                "Metric": "Execution Time",
                "Value": energy["duration"],
                "Unit": "seconds"
            },
            {
                "Category": "Energy Monitoring",
                "Metric": "Energy Consumption",
                "Value": energy["energy"],
                "Unit": "kWh"
            },
            {
                "Category": "Energy Monitoring",
                "Metric": "CO2 Emissions",
                "Value": energy["co2"],
                "Unit": "kg CO2e"
            },
            {
                "Category": "Energy Monitoring",
                "Metric": "CPU Energy",
                "Value": energy["cpu_energy"],
                "Unit": "kWh"
            },
            {
                "Category": "Energy Monitoring",
                "Metric": "RAM Energy",
                "Value": energy["ram_energy"],
                "Unit": "kWh"
            },
            {
                "Category": "Code Comparison",
                "Metric": "Original Execution Time",
                "Value": original["time"],
                "Unit": "seconds"
            },
            {
                "Category": "Code Comparison",
                "Metric": "Optimized Execution Time",
                "Value": optimized["time"],
                "Unit": "seconds"
            },
            {
                "Category": "Code Comparison",
                "Metric": "Original Energy",
                "Value": original["energy"],
                "Unit": "kWh"
            },
            {
                "Category": "Code Comparison",
                "Metric": "Optimized Energy",
                "Value": optimized["energy"],
                "Unit": "kWh"
            },
            {
                "Category": "Code Comparison",
                "Metric": "Original CO2",
                "Value": original["emissions"],
                "Unit": "kg CO2e"
            },
            {
                "Category": "Code Comparison",
                "Metric": "Optimized CO2",
                "Value": optimized["emissions"],
                "Unit": "kg CO2e"
            },
            {
                "Category": "Code Comparison",
                "Metric": "Results Match",
                "Value": comparison["results_match"],
                "Unit": "Boolean"
            },
            {
                "Category": "Code Comparison",
                "Metric": "Energy Reduction",
                "Value": comparison["energy_reduction"],
                "Unit": "%"
            },
            {
                "Category": "Code Comparison",
                "Metric": "CO2 Reduction",
                "Value": comparison["emission_reduction"],
                "Unit": "%"
            }
        ])

        st.success("Complete analysis report generated!")

        st.dataframe(
            complete_report,
            use_container_width=True
        )

        st.download_button(
            label="Download Complete Green Software Report",
            data=complete_report.to_csv(index=False),
            file_name="Complete_GreenCode_Analysis.csv",
            mime="text/csv"
        )

else:

    st.info(
        "Please complete Static Analysis, Energy Monitoring "
        "and Code Comparison before generating the complete report."
    )
# ==========================================
# MODULE 6: INDUSTRIAL ENERGY & CARBON ANALYSIS
# ==========================================

st.divider()

st.header("6. Industrial Energy & Carbon Analysis")

st.write(
    "Analyze steel factory energy consumption, "
    "carbon emissions and potential sustainable improvements."
)

st.warning(
    "The production and energy intensity defaults are based on "
    "the illustrative example shared by the teacher. "
    "Carbon emission inputs must be supplied separately."
)

# FACTORY INPUTS

st.subheader("Factory Energy Inputs")

with st.form("industrial_analysis_form"):

    col1, col2 = st.columns(2)

    annual_production = col1.number_input(
        "Annual Production (tonnes)",
        min_value=0.01,
        value=500000.0,
        step=1000.0
    )

    energy_intensity = col2.number_input(
        "Energy Intensity (GJ per tonne)",
        min_value=0.01,
        value=20.95,
        step=0.1
    )

    energy_reduction = col1.number_input(
        "Expected Energy Improvement (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0
    )

    emission_reduction = col2.number_input(
        "Expected Emission Improvement (%)",
        min_value=0.0,
        max_value=100.0,
        value=5.0
    )

    # CARBON INPUTS

    st.subheader("Electricity and Fuel Inputs")

    col3, col4 = st.columns(2)

    electricity_kwh = col3.number_input(
        "Electricity Consumption (kWh)",
        min_value=0.0,
        value=0.0
    )

    electricity_factor = col4.number_input(
        "Electricity Emission Factor (kg CO2/kWh)",
        min_value=0.0,
        value=0.0
    )

    fuel_energy_gj = col3.number_input(
        "Fuel Energy Consumption (GJ)",
        min_value=0.0,
        value=0.0
    )

    fuel_factor = col4.number_input(
        "Fuel Emission Factor (kg CO2/GJ)",
        min_value=0.0,
        value=0.0
    )

    submitted = st.form_submit_button(
        "Generate Industrial Report",
        type="primary"
    )


# CALCULATIONS

if submitted:

    try:

        factory = calculate_factory_energy(
            annual_production,
            energy_intensity,
            energy_reduction
        )

        carbon = calculate_carbon_emissions(
            electricity_kwh,
            electricity_factor,
            fuel_energy_gj,
            fuel_factor
        )

        improvement = simulate_improvement(
            factory["annual_energy_kwh_equivalent"],
            carbon["total_emissions_kg"],
            energy_reduction,
            emission_reduction
        )

        st.session_state.industrial_results = {
            "factory": factory,
            "carbon": carbon,
            "improvement": improvement
        }

        st.success("Industrial analysis completed successfully!")

    except Exception as error:

        st.error(f"Industrial analysis failed: {error}")


# DISPLAY RESULTS

industrial_results = st.session_state.get("industrial_results")

if industrial_results:

    factory = industrial_results["factory"]
    carbon = industrial_results["carbon"]
    improvement = industrial_results["improvement"]

    st.divider()
    st.subheader("Industrial Analysis Results")

    col1, col2 = st.columns(2)

    col1.metric(
        "Annual Energy",
        f"{factory['annual_energy_gj']:,.2f} GJ"
    )

    col2.metric(
        "Annual Energy Equivalent",
        f"{factory['annual_energy_kwh_equivalent']:,.2f} kWh"
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "Daily Energy Equivalent",
        f"{factory['daily_energy_kwh_equivalent']:,.2f} kWh"
    )

    col4.metric(
        "Total Carbon Emissions",
        f"{carbon['total_emissions_tonnes']:,.2f} tonnes"
    )

    # BEFORE VS AFTER COMPARISON

    st.subheader("Before vs After Improvement")

    col5, col6 = st.columns(2)

    col5.metric(
        "Energy Saved",
        f"{improvement['energy_saved']:,.2f} kWh-equivalent"
    )

    col6.metric(
        "Emissions Saved",
        f"{improvement['emissions_saved']:,.2f} kg CO2"
    )

    energy_data = pd.DataFrame(
        {
            "Energy (kWh-equivalent)": [
                improvement["baseline_energy"],
                improvement["optimized_energy"]
            ]
        },
        index=["Before Improvement", "After Improvement"]
    )

    st.write("Energy Comparison")
    st.bar_chart(energy_data)

    emission_data = pd.DataFrame(
        {
            "Emissions (kg CO2)": [
                improvement["baseline_emissions"],
                improvement["optimized_emissions"]
            ]
        },
        index=["Before Improvement", "After Improvement"]
    )

    st.write("Carbon Emission Comparison")
    st.bar_chart(emission_data)

    # DOWNLOAD REPORT

    industrial_report = pd.DataFrame([
        {
            "Metric": "Annual Production",
            "Value": factory["annual_production"],
            "Unit": "tonnes"
        },
        {
            "Metric": "Energy Intensity",
            "Value": factory["energy_intensity"],
            "Unit": "GJ/tonne"
        },
        {
            "Metric": "Annual Energy",
            "Value": factory["annual_energy_gj"],
            "Unit": "GJ"
        },
        {
            "Metric": "Annual Energy Equivalent",
            "Value": factory["annual_energy_kwh_equivalent"],
            "Unit": "kWh-equivalent"
        },
        {
            "Metric": "Electricity Emissions",
            "Value": carbon["electricity_emissions_kg"],
            "Unit": "kg CO2"
        },
        {
            "Metric": "Fuel Emissions",
            "Value": carbon["fuel_emissions_kg"],
            "Unit": "kg CO2"
        },
        {
            "Metric": "Total Carbon Emissions",
            "Value": carbon["total_emissions_kg"],
            "Unit": "kg CO2"
        },
        {
            "Metric": "Energy Saved",
            "Value": improvement["energy_saved"],
            "Unit": "kWh-equivalent"
        },
        {
            "Metric": "Optimized Energy",
            "Value": improvement["optimized_energy"],
            "Unit": "kWh-equivalent"
        },
        {
            "Metric": "Emissions Saved",
            "Value": improvement["emissions_saved"],
            "Unit": "kg CO2"
        },
        {
            "Metric": "Optimized Emissions",
            "Value": improvement["optimized_emissions"],
            "Unit": "kg CO2"
        }
    ])

    st.subheader("Download Industrial Report")

    st.dataframe(
        industrial_report,
        use_container_width=True
    )

    st.download_button(
        label="Download Industrial Report CSV",
        data=industrial_report.to_csv(index=False),
        file_name="Industrial_Sustainability_Report.csv",
        mime="text/csv"
    )

    st.caption(
        "The improvement results are simulations, not measured savings. "
        "Energy in kWh-equivalent is not electricity-meter consumption. "
        "Use verified emission factors and actual factory data for "
        "a real carbon assessment."
    )

# ==========================================
# MODULE 7: PROCESS-WISE ENERGY ANALYSIS
# ==========================================

st.divider()
st.header("7. Process-wise Energy Analysis")

st.write(
    "Identify which industrial process consumes the most energy "
    "and compare the share of each process."
)

st.info(
    "The default values below are illustrative sample data. "
    "Replace them with actual process-wise measurements before "
    "using the results as a factory assessment."
)

with st.form("process_energy_form"):
    st.subheader("Enter Process Energy Consumption (GJ)")

    col1, col2 = st.columns(2)

    furnace_energy = col1.number_input(
        "Furnace Energy (GJ)", min_value=0.0, value=500.0
    )
    rolling_energy = col2.number_input(
        "Rolling Mill Energy (GJ)", min_value=0.0, value=300.0
    )
    motors_energy = col1.number_input(
        "Motors and Pumps Energy (GJ)", min_value=0.0, value=150.0
    )
    compressed_air_energy = col2.number_input(
        "Compressed Air Energy (GJ)", min_value=0.0, value=50.0
    )

    process_submitted = st.form_submit_button(
        "Analyze Process Energy", type="primary"
    )

if process_submitted:
    try:
        process_data = {
            "Furnace": furnace_energy,
            "Rolling Mill": rolling_energy,
            "Motors and Pumps": motors_energy,
            "Compressed Air": compressed_air_energy
        }

        process_results = analyze_process_energy(process_data)
        st.session_state.process_energy_results = process_results
        st.success("Process-wise energy analysis completed!")

    except Exception as error:
        st.error(f"Process analysis failed: {error}")

process_results = st.session_state.get("process_energy_results")

if process_results:
    st.subheader("Process-wise Results")

    st.metric(
        "Total Entered Process Energy",
        f"{process_results['total_energy_gj']:,.2f} GJ"
    )

    st.metric(
        "Highest Energy-consuming Process",
        process_results["highest_energy_process"],
        f"{process_results['highest_energy_value_gj']:,.2f} GJ"
    )

    process_table = pd.DataFrame([
        {
            "Process": process,
            "Energy (GJ)": details["energy_gj"],
            "Energy Share (%)": details["share_percent"]
        }
        for process, details in process_results["process_results"].items()
    ])

    st.dataframe(process_table, use_container_width=True)

    st.bar_chart(
        process_table.set_index("Process")["Energy (GJ)"]
    )

    st.download_button(
        label="Download Process-wise Energy Report",
        data=process_table.to_csv(index=False),
        file_name="Process_Wise_Energy_Report.csv",
        mime="text/csv"
    )

    st.caption(
        "Process-wise values should represent the same reporting period "
        "and energy boundary. Do not combine sample values with the "
        "factory-wide energy baseline unless their scope and units match."
    )

# ==========================================
# MODULE 8: INDUSTRIAL SUSTAINABILITY RECOMMENDATIONS
# ==========================================

st.divider()
st.header("8. Industrial Sustainability Recommendations")

st.write(
    "Get process-specific recommendations to identify "
    "potential industrial energy-saving opportunities."
)

process_results = st.session_state.get("process_energy_results")

if process_results:

    recommendations = generate_process_recommendations(
        process_results
    )

    st.subheader("Recommended Improvement Actions")

    for item in recommendations:

        st.markdown(f"### {item['process']}")

        st.write(
            f"Energy Consumption Share: "
            f"{item['energy_share']:.2f}%"
        )

        st.info(item["recommendation"])

else:

    st.warning(
        "Please complete Process-wise Energy Analysis in Module 7 first."
    )

# ==========================================
# MODULE 9: BEFORE VS AFTER SIMULATION
# ==========================================

st.divider()
st.header("9. Before vs After Sustainability Simulation")

st.write(
    "Simulate the impact of sustainable improvements "
    "on each industrial process."
)

process_results = st.session_state.get("process_energy_results")

if process_results:

    process_data = {
        process: details["energy_gj"]
        for process, details in process_results["process_results"].items()
    }

    st.subheader("Set Improvement Percentage")

    st.info(
        "These percentages are simulation assumptions, "
        "not measured or guaranteed energy savings."
    )

    with st.form("sustainability_simulation_form"):

        improvement_percentages = {}

        for process, energy in process_data.items():

            improvement_percentages[process] = st.number_input(
                f"{process} Improvement (%)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=1.0
            )

        simulation_submitted = st.form_submit_button(
            "Run Sustainability Simulation",
            type="primary"
        )

    if simulation_submitted:

        try:
            simulation = simulate_process_improvements(
                process_data,
                improvement_percentages
            )

            st.session_state.sustainability_simulation = simulation

            st.success("Sustainability simulation completed!")

        except Exception as error:
            st.error(f"Simulation failed: {error}")

    simulation = st.session_state.get("sustainability_simulation")

    if simulation:

        st.subheader("Before vs After Results")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Before Improvement",
            f"{simulation['total_before_gj']:,.2f} GJ"
        )

        col2.metric(
            "After Improvement",
            f"{simulation['total_after_gj']:,.2f} GJ"
        )

        col3.metric(
            "Total Energy Saved",
            f"{simulation['total_saved_gj']:,.2f} GJ",
            f"{simulation['overall_reduction_percent']:.2f}% reduction"
        )

        simulation_table = pd.DataFrame([
            {
                "Process": process,
                "Before (GJ)": details["before_gj"],
                "Improvement (%)": details["improvement_percent"],
                "Energy Saved (GJ)": details["energy_saved_gj"],
                "After (GJ)": details["after_gj"]
            }
            for process, details
            in simulation["process_results"].items()
        ])

        st.dataframe(
            simulation_table,
            use_container_width=True
        )

        st.subheader("Energy Consumption Comparison")

        comparison_chart = simulation_table.set_index("Process")[
            ["Before (GJ)", "After (GJ)"]
        ]

        st.bar_chart(comparison_chart)

        st.download_button(
            label="Download Sustainability Simulation Report",
            data=simulation_table.to_csv(index=False),
            file_name="Sustainability_Simulation_Report.csv",
            mime="text/csv"
        )

else:

    st.warning(
        "Please complete Process-wise Energy Analysis in Module 7 first."
    )

# ==========================================
# MODULE 10: INDUSTRIAL CARBON REDUCTION
# ==========================================

st.divider()
st.header("10. Industrial Carbon Reduction Analysis")

st.write(
    "Calculate process-wise carbon emissions and simulate "
    "potential CO2 reduction after sustainable improvements."
)

st.info(
    "Enter electricity and fuel consumption for each process. "
    "The default values and emission factors are illustrative "
    "testing assumptions, not verified factory measurements."
)

process_names = [
    "Furnace",
    "Rolling Mill",
    "Motors and Pumps",
    "Compressed Air"
]

with st.form("industrial_carbon_form"):

    st.subheader("Process-wise Carbon Inputs")

    carbon_inputs = {}

    for process in process_names:

        st.markdown(f"### {process}")

        col1, col2 = st.columns(2)

        electricity = col1.number_input(
            f"{process} Electricity (kWh)",
            min_value=0.0,
            value=0.0,
            key=f"carbon_electricity_{process}"
        )

        fuel = col2.number_input(
            f"{process} Fuel Energy (GJ)",
            min_value=0.0,
            value=0.0,
            key=f"carbon_fuel_{process}"
        )

        col3, col4 = st.columns(2)

        electricity_factor = col3.number_input(
            f"{process} Electricity Factor (kg CO2/kWh)",
            min_value=0.0,
            value=0.0,
            key=f"carbon_ef_{process}"
        )

        fuel_factor = col4.number_input(
            f"{process} Fuel Factor (kg CO2/GJ)",
            min_value=0.0,
            value=0.0,
            key=f"carbon_ff_{process}"
        )

        improvement = st.number_input(
            f"{process} Emission Improvement (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            key=f"carbon_improvement_{process}"
        )

        carbon_inputs[process] = {
            "electricity_kwh": electricity,
            "fuel_gj": fuel,
            "electricity_factor": electricity_factor,
            "fuel_factor": fuel_factor,
            "improvement_percent": improvement
        }

    carbon_submitted = st.form_submit_button(
        "Calculate Carbon Reduction",
        type="primary"
    )

if carbon_submitted:

    try:

        carbon_results = calculate_process_carbon_reduction(
            carbon_inputs
        )

        st.session_state.industrial_carbon_results = carbon_results

        st.success("Industrial carbon analysis completed!")

    except Exception as error:

        st.error(f"Carbon analysis failed: {error}")

carbon_results = st.session_state.get(
    "industrial_carbon_results"
)

if carbon_results:

    st.subheader("Before vs After Carbon Results")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Before Improvement",
        f"{carbon_results['total_before_kg']:,.2f} kg"
    )

    col2.metric(
        "After Improvement",
        f"{carbon_results['total_after_kg']:,.2f} kg"
    )

    col3.metric(
        "CO2 Saved",
        f"{carbon_results['total_saved_kg']:,.2f} kg",
        f"{carbon_results['reduction_percent']:.2f}% reduction"
    )

    st.metric(
        "Total CO2 Saved (Tonnes)",
        f"{carbon_results['total_saved_tonnes']:,.4f}"
    )

    carbon_table = pd.DataFrame([
        {
            "Process": process,
            "Before (kg CO2)": details["before_kg"],
            "After (kg CO2)": details["after_kg"],
            "CO2 Saved (kg)": details["saved_kg"],
            "Reduction (%)": details["improvement_percent"]
        }
        for process, details
        in carbon_results["process_results"].items()
    ])

    st.subheader("Process-wise Carbon Comparison")

    st.dataframe(
        carbon_table,
        use_container_width=True
    )

    st.bar_chart(
        carbon_table.set_index("Process")[
            ["Before (kg CO2)", "After (kg CO2)"]
        ]
    )

    st.download_button(
        label="Download Carbon Reduction Report",
        data=carbon_table.to_csv(index=False),
        file_name="Industrial_Carbon_Reduction_Report.csv",
        mime="text/csv"
    )

# ==========================================
# MODULE 11: COMBINED INDUSTRIAL REPORT
# ==========================================

st.divider()
st.header("11. Combined Industrial Sustainability Report")

st.write(
    "Generate a consolidated report using the results "
    "of the industrial analysis modules."
)

if st.button("Generate Combined Industrial Report"):

    factory_results = st.session_state.get("factory_results")
    process_results = st.session_state.get("process_energy_results")
    energy_simulation = st.session_state.get("industrial_simulation_results")
    carbon_results = st.session_state.get("industrial_carbon_results")
    recommendations = st.session_state.get("industrial_recommendations")

    missing = []

    if not factory_results:
        missing.append("Factory Energy Analysis (Module 6)")

    if not process_results:
        missing.append("Process Energy Analysis (Module 7)")

    if not energy_simulation:
        missing.append("Sustainability Simulation (Module 9)")

    if not carbon_results:
        missing.append("Carbon Reduction Analysis (Module 10)")

    if not recommendations:
        missing.append("Sustainability Recommendations (Module 8)")

    if missing:
        st.warning(
            "Please run these modules first: "
            + ", ".join(missing)
        )

    else:
        report_text = generate_combined_report(
            factory_results,
            process_results,
            recommendations,
            energy_simulation,
            carbon_results
        )

        st.session_state.combined_industrial_report = report_text

if st.session_state.get("combined_industrial_report"):

    st.subheader("Generated Sustainability Report")

    st.text(st.session_state.combined_industrial_report)

    st.download_button(
        label="Download Combined Industrial Report",
        data=st.session_state.combined_industrial_report,
        file_name="Combined_Industrial_Sustainability_Report.txt",
        mime="text/plain"
    )

    st.success("Combined report is ready!")
