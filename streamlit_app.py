import streamlit as st
import sqlite3
import pandas as pd

# =====================
# DATABASE
# =====================
conn = sqlite3.connect("trip.db", check_same_thread=False)
c = conn.cursor()

# tabel trip
c.execute("""
CREATE TABLE IF NOT EXISTS trip(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nama TEXT,
kategori TEXT,
tanggal TEXT,
harga INTEGER
)
""")

# tabel peserta
c.execute("""
CREATE TABLE IF NOT EXISTS peserta(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nama TEXT,
usia INTEGER,
hp TEXT,
trip TEXT
)
""")
conn.commit()

# =====================
# SIDEBAR
# =====================
menu = st.sidebar.selectbox(
    "Menu",
    ["Beranda","Trip","Admin"]
)

# =====================
# BERANDA
# =====================
if menu=="Beranda":

    st.title("🏔 OPEN TRIP GUNUNG & CURUG")

    st.image(
        "https://images.unsplash.com/photo-1464822759023-fed622ff2c3",
        use_container_width=True
    )

    st.write("""
    Selamat datang di Open Trip Adventure.

    Kami menyediakan perjalanan:
    - Pendakian gunung
    - Wisata curug
    - Trip bersama komunitas
    """)

# =====================
# MENU TRIP
# =====================
elif menu=="Trip":

    st.title("Daftar Trip")

    df = pd.read_sql("SELECT * FROM trip", conn)

    if len(df)==0:
        st.warning("Belum ada trip.")
    else:

        for i,row in df.iterrows():

            with st.container():

                st.subheader(row["nama"])
                st.write("Kategori :",row["kategori"])
                st.write("Tanggal :",row["tanggal"])
                st.write("Harga : Rp{:,.0f}".format(row["harga"]))

                with st.expander("Daftar Sekarang"):

                    nama = st.text_input(
                        "Nama",
                        key=f"nama{i}"
                    )

                    usia = st.number_input(
                        "Usia",
                        10,
                        80,
                        key=f"usia{i}"
                    )

                    hp = st.text_input(
                        "No Handphone",
                        key=f"hp{i}"
                    )

                    if st.button(
                        "Daftar",
                        key=f"daftar{i}"
                    ):

                        c.execute(
                        """
                        INSERT INTO peserta
                        (nama,usia,hp,trip)
                        VALUES(?,?,?,?)
                        """,
                        (nama,usia,hp,row["nama"])
                        )

                        conn.commit()

                        st.success("Pendaftaran berhasil")

# =====================
# ADMIN
# =====================
elif menu=="Admin":

    st.title("Admin Panel")

    user = st.text_input("Username")
    pw = st.text_input("Password",type="password")

    if user=="admin" and pw=="admin123":

        st.success("Login berhasil")

        tab1,tab2,tab3 = st.tabs([
            "Tambah Trip",
            "Data Trip",
            "Peserta"
        ])

        # tambah trip
        with tab1:

            nama = st.text_input("Nama Trip")

            kategori = st.selectbox(
                "Kategori",
                ["Gunung","Curug"]
            )

            tanggal = st.date_input(
                "Tanggal Berangkat"
            )

            harga = st.number_input(
                "Harga"
            )

            if st.button("Tambah Trip"):

                c.execute(
                """
                INSERT INTO trip
                (nama,kategori,tanggal,harga)
                VALUES(?,?,?,?)
                """,
                (
                nama,
                kategori,
                str(tanggal),
                harga
                )
                )

                conn.commit()

                st.success("Trip berhasil ditambahkan")

        # data trip
        with tab2:

            df = pd.read_sql(
                "SELECT * FROM trip",
                conn
            )

            st.dataframe(df)

        # peserta
        with tab3:

            peserta = pd.read_sql(
                "SELECT * FROM peserta",
                conn
            )

            st.dataframe(peserta)

    else:
        st.info("Silakan login admin")
