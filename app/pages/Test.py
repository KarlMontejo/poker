import streamlit as st 
import time
import pandas as pd
import numpy as np
st.markdown("C1")
c1 = st.empty()
with c1:
    st.info("A1")
st.markdown("C2")
c2 = st.empty()
c2.info("c2")
st.markdown("C3")
c3 = st.empty()
c3.info('c3')
st.markdown("C4")
c4 = st.empty()
c4.info('c4')
time.sleep(3)
with c1.container():
    st.info('c1.2')
    st.info('c1.3')

time.sleep(3)

with c1:
    st.success("Done")
