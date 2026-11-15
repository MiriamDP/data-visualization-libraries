
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.set_page_config(
    page_title="Comparador de gráficos",
    page_icon="📊",
    layout="wide"
)

sns.set_theme(style="whitegrid")


@st.cache_data
def cargar_datos():
    df = pd.read_csv("sales.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


df = cargar_datos()


st.title("📊 Comparador de bibliotecas de visualización")

st.write("""
Comparación de Matplotlib, Seaborn, Plotly y Streamlit
utilizando un mismo conjunto de datos de ventas.
""")

c1, c2, c3 = st.columns(3)

c1.metric("Transacciones", len(df))
c2.metric("Clientes únicos", df["Customer ID"].nunique())
c3.metric(
    "Ventas totales",
    f"{df['Total Amount'].sum():,.0f} €"
)

st.divider()

opcion = st.selectbox(
    "Selecciona el análisis que quieres comparar:",
    [
        "Ventas por categoría",
        "Distribución de edades",
        "Ventas por género",
        "Edad frente a gasto",
        "Evolución de ventas",
        "Cantidad por categoría",
        "Distribución del gasto"
    ]
)

st.subheader(f"Comparación: {opcion}")


ventas = (
    df.groupby("Product Category", as_index=False)["Total Amount"]
    .sum()
)

genero = (
    df.groupby("Gender", as_index=False)["Total Amount"]
    .sum()
)

cantidad = (
    df.groupby("Product Category", as_index=False)["Quantity"]
    .sum()
)

ventas_fecha = (
    df.groupby("Date", as_index=False)["Total Amount"]
    .sum()
    .sort_values("Date")
)


tab1, tab2, tab3, tab4 = st.tabs(
    ["Matplotlib", "Seaborn", "Plotly", "Streamlit"]
)

with tab1:

    st.subheader("Visualización con Matplotlib")

    fig, ax = plt.subplots(figsize=(9, 5))

    if opcion == "Ventas por categoría":

        ax.bar(
            ventas["Product Category"],
            ventas["Total Amount"],
            color="skyblue"
        )

        ax.set_ylabel("Ventas totales (€)")

    elif opcion == "Distribución de edades":

        ax.hist(
            df["Age"],
            bins=15,
            color="orange",
            edgecolor="black"
        )

        ax.set_xlabel("Edad")
        ax.set_ylabel("Frecuencia")

    elif opcion == "Ventas por género":

        ax.pie(
            genero["Total Amount"],
            labels=genero["Gender"],
            autopct="%1.1f%%"
        )

    elif opcion == "Edad frente a gasto":

        ax.scatter(
            df["Age"],
            df["Total Amount"],
            alpha=0.6,
            color="purple"
        )

        ax.set_xlabel("Edad")
        ax.set_ylabel("Importe (€)")

    elif opcion == "Evolución de ventas":

        ax.plot(
            ventas_fecha["Date"],
            ventas_fecha["Total Amount"],
            color="green"
        )

        ax.set_xlabel("Fecha")
        ax.set_ylabel("Ventas (€)")

        plt.xticks(rotation=45)

    elif opcion == "Cantidad por categoría":

        ax.barh(
            cantidad["Product Category"],
            cantidad["Quantity"],
            color="coral"
        )

    elif opcion == "Distribución del gasto":

        categorias = df["Product Category"].unique()

        datos = [
            df[df["Product Category"] == cat]["Total Amount"]
            for cat in categorias
        ]

        ax.boxplot(
            datos,
            tick_labels=categorias
        )

    ax.set_title(opcion)

    fig.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


with tab2:

    st.subheader("Visualización con Seaborn")

    fig, ax = plt.subplots(figsize=(9, 5))

    if opcion == "Ventas por categoría":

        sns.barplot(
            data=df,
            x="Product Category",
            y="Total Amount",
            estimator=sum,
            errorbar=None,
            ax=ax
        )

    elif opcion == "Distribución de edades":

        sns.histplot(
            data=df,
            x="Age",
            bins=15,
            kde=True,
            ax=ax
        )

    elif opcion == "Ventas por género":

        ax.pie(
            genero["Total Amount"],
            labels=genero["Gender"],
            autopct="%1.1f%%",
            colors=sns.color_palette("pastel")
        )

    elif opcion == "Edad frente a gasto":

        sns.scatterplot(
            data=df,
            x="Age",
            y="Total Amount",
            hue="Gender",
            ax=ax
        )

    elif opcion == "Evolución de ventas":

        sns.lineplot(
            data=ventas_fecha,
            x="Date",
            y="Total Amount",
            ax=ax
        )

        plt.xticks(rotation=45)

    elif opcion == "Cantidad por categoría":

        sns.barplot(
            data=df,
            y="Product Category",
            x="Quantity",
            estimator=sum,
            errorbar=None,
            ax=ax
        )

    elif opcion == "Distribución del gasto":

        sns.boxplot(
            data=df,
            x="Product Category",
            y="Total Amount",
            ax=ax
        )

    ax.set_title(opcion)

    fig.tight_layout()

    st.pyplot(fig)

    plt.close(fig)


with tab3:

    st.subheader("Visualización con Plotly")

    if opcion == "Ventas por categoría":

        fig = px.bar(
            ventas,
            x="Product Category",
            y="Total Amount",
            color="Product Category",
            title=opcion
        )

    elif opcion == "Distribución de edades":

        fig = px.histogram(
            df,
            x="Age",
            nbins=15,
            title=opcion
        )

    elif opcion == "Ventas por género":

        fig = px.pie(
            genero,
            names="Gender",
            values="Total Amount",
            hole=0.3,
            title=opcion
        )

    elif opcion == "Edad frente a gasto":

        fig = px.scatter(
            df,
            x="Age",
            y="Total Amount",
            color="Gender",
            hover_data=["Customer ID"],
            title=opcion
        )

    elif opcion == "Evolución de ventas":

        fig = px.line(
            ventas_fecha,
            x="Date",
            y="Total Amount",
            markers=True,
            title=opcion
        )

    elif opcion == "Cantidad por categoría":

        fig = px.bar(
            cantidad,
            x="Quantity",
            y="Product Category",
            orientation="h",
            title=opcion
        )

    elif opcion == "Distribución del gasto":

        fig = px.box(
            df,
            x="Product Category",
            y="Total Amount",
            color="Product Category",
            title=opcion
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with tab4:

    st.subheader("Visualización con Streamlit")

    st.write("""
    Streamlit permite crear una aplicación interactiva
    y visualizar datos mediante gráficos nativos,
    métricas, tablas y filtros.
    """)

    if opcion == "Ventas por categoría":

        st.bar_chart(
            ventas,
            x="Product Category",
            y="Total Amount"
        )

    elif opcion == "Distribución de edades":

        edades = (
            df["Age"]
            .value_counts()
            .sort_index()
            .rename_axis("Edad")
            .reset_index(name="Frecuencia")
        )

        st.bar_chart(
            edades,
            x="Edad",
            y="Frecuencia"
        )

    elif opcion == "Ventas por género":

        st.write("Distribución de ventas por género")

        st.dataframe(
            genero,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Ventas totales",
            f"{genero['Total Amount'].sum():,.0f} €"
        )

    elif opcion == "Edad frente a gasto":

        st.scatter_chart(
            df,
            x="Age",
            y="Total Amount",
            color="Gender"
        )

    elif opcion == "Evolución de ventas":

        st.line_chart(
            ventas_fecha.set_index("Date")["Total Amount"]
        )

    elif opcion == "Cantidad por categoría":

        st.bar_chart(
            cantidad,
            x="Product Category",
            y="Quantity"
        )

    elif opcion == "Distribución del gasto":

        st.write("Estadísticas del gasto por categoría")

        resumen = (
            df.groupby("Product Category")["Total Amount"]
            .describe()
            .round(2)
        )

        st.dataframe(
            resumen,
            use_container_width=True
        )

    st.caption(
        "Los gráficos nativos de Streamlit se utilizan "
        "cuando están disponibles. Para otros tipos de "
        "visualización se muestran métricas o tablas."
    )

st.divider()

with st.expander("Consultar dataframe original"):

    st.dataframe(
        df,
        use_container_width=True
    )


st.caption(
    "Proyecto de comparación de visualización de datos."
)
