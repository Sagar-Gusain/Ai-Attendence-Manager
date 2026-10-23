import dlib
from PIL import Image
import numpy as np
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_student_faces