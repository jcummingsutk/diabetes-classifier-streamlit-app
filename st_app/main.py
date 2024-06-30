import json
import os

import requests
import streamlit as st


def set_config():
    st.set_page_config(page_title="BRFSS Diabetes Questionnaire and Predictor")
    st.header("BRFSS Diabetes Questionnaire and Predictor")
    st.write(
        "Below are questions from the [Questionnaire](https://www.cdc.gov/brfss/annual_data/2015/pdf/codebook15_llcp.pdf) that are used in the model. As you change the values, you can see the JSON data that are sent to the model as input in the sidebar. When you click on the 'Run Model' button on the sidebar, the displayed JSON data get sent to the API for the model, and the model returns its response. "
    )


def main():
    set_config()
    with open(os.path.join("st_app", "questions.json")) as fp:
        questions_dict = json.load(fp)
    default = {
        "HighBP": 0,
        "HighChol": 0,
        "BMI": 21,
        "Smoker": 0,
        "Stroke": 0,
        "HeartDiseaseorAttack": 0,
        "PhysActivity": 0,
        "Fruits": 1,
        "Veggies": 1,
        "NoDocbcCost": 0,
        "MentHlth": 3,
        "GenHlth": 3,
        "PhysHlth": 7,
        "DiffWalk": 0,
        "Sex": 0,
        "Age": 7,
        "Education": 4,
        "Income": 2,
    }

    json_payload_as_dict = default
    for json_payload_key, question_data in questions_dict.items():
        if question_data["type"] == "multiselect":
            vals = question_data["possibleValues"].keys()
            response = st.selectbox(
                label=question_data["question"],
                options=vals,
            )
            json_payload_as_dict[json_payload_key] = question_data["possibleValues"][
                response
            ]
        elif question_data["type"] == "integer":
            min_ = question_data["possibleValues"]["min"]
            max_ = question_data["possibleValues"]["max"]
            default = question_data["possibleValues"]["default"]
            value = st.number_input(
                label=question_data["question"],
                min_value=min_,
                max_value=max_,
                value=default,
            )
            json_payload_as_dict[json_payload_key] = value
    with st.sidebar:
        st.write(
            "Here you can see how the responses that you make to the right change the JSON data sent to the API for the model"
        )
        st.write("JSON data sent to the API:")
        st.write(json_payload_as_dict)
        if st.button("Run Model"):
            with st.spinner("Processing"):
                r = requests.post(
                    "https://king-prawn-app-2-y4ac7.ondigitalocean.app/single_prediction",
                    json=json_payload_as_dict,
                )
                if r.status_code == 200:
                    result = r.json()
                    proba = result["probabilityPrediction"]
                    if result["prediction"] == 0:
                        st.write(
                            f"The model predicts **no diabetes**, and a predicted probability of diabetes is {proba*100:.0f}%. However, this is a model written as a side project by someone who has no medical knowledge. Trust your doctor!"
                        )
                    if result["prediction"] == 1:
                        st.write(
                            f"The model predicts **diabetes**, and a predicted probability of diabetes is {proba*100:.0f}%. However, this is a model written as a side project by someone who has no medical knowledge. Trust your doctor!"
                        )
    return


if __name__ == "__main__":
    main()
