import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { microservices as lessons } from "../services/mockMicroservices";

export default function AddWord() {
  const navigate = useNavigate();

  const [word, setWord] = useState("");
  const [meaning, setMeaning] = useState("");
  const [selected, setSelected] = useState(null);

  return (
    <div className="t9-page" dir="rtl" lang="fa">
      <header className="t9-topbar">
        <button className="t9-pillBtn">حساب کاربری</button>
        <h1 className="t9-title">یادگیری مستمر با Tick 8</h1>
        <button className="t9-pillBtn" onClick={() => navigate("/microservices")}>
          خانه
        </button>
      </header>

      <section className="t9-panel t9-addword">
        <div className="t9-form">
          <label className="t9-label">
            <span>Enter Word:</span>
            <input
              className="t9-input"
              value={word}
              onChange={(e) => setWord(e.target.value)}
            />
          </label>

          <label className="t9-label">
            <span>معنی واژه:</span>
            <input
              className="t9-input"
              value={meaning}
              onChange={(e) => setMeaning(e.target.value)}
            />
          </label>

          <div className="t9-label">
            <span>انتخاب درس مورد نظر:</span>
          </div>

          <div className="t9-lessonBox">
            {lessons.map((l) => (
              <button
                key={l.id}
                type="button"
                className={`t9-lessonBtn ${selected === l.id ? "is-active" : ""}`}
                onClick={() => setSelected(l.id)}
              >
                {l.title}
              </button>
            ))}
          </div>

          <div className="t9-addwordActions">
            <button className="t9-actionBtn" type="button" onClick={() => navigate(-1)}>
              بازگشت
            </button>

            <button
              className="t9-actionBtn"
              type="button"
              onClick={() => {
                
                console.log({ word, meaning, selected });
                alert("فعلا mock است. بعدا به API وصل می‌کنیم.");
              }}
            >
              افزودن واژه
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
