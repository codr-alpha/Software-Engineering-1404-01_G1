import { useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { microservices } from "../services/mockMicroservices";

export default function ReviewLesson() {
  const { id } = useParams();
  const navigate = useNavigate();

  const lesson = useMemo(() => {
    const numId = Number(id);
    return microservices.find((x) => x.id === numId) || null;
  }, [id]);


  const words = useMemo(() => {
    const fallback = [
      { en: "Vacation", fa: "تعطیلات" },
      { en: "Sightseeing", fa: "گردشگری" },
      { en: "Departure", fa: "عزیمت" },
      { en: "Destination", fa: "مقصد" },
    ];
    return lesson?.wordList?.length ? lesson.wordList : fallback;
  }, [lesson]);

  const [index, setIndex] = useState(0);
  const [cells, setCells] = useState(
    Array.from({ length: 8 }, () => "empty")
  );

  if (!lesson) return null;

  const word = words[index];

  const mark = (type) => {
    setCells((prev) => {
      const next = [...prev];
      const last = next.length - 1;
      next[last] = type === "know" ? "green" : "orange";
      return next;
    });
  };

  return (
    <div className="t9-page" dir="rtl" lang="fa">
      <header className="t9-topbar">
        <button className="t9-pillBtn" onClick={() => navigate(`/microservices/${id}`)}>
          بازگشت
        </button>
        <h1 className="t9-title">{lesson.title}</h1>
        <button className="t9-pillBtn" onClick={() => navigate("/microservices")}>
          خانه
        </button>
      </header>

      <section className="t9-panel t9-reviewBox">
        <h2 className="t9-reviewWord">{word.en}</h2>

        <div className="t9-reviewActions">
          <button
            className="t9-chip t9-chip--green"
            onClick={() => mark("know")}
          >
            میدانم
          </button>
          <button
            className="t9-chip t9-chip--orange"
            onClick={() => mark("dont")}
          >
            نمیدانم
          </button>
        </div>

        <div className="t9-cells t9-cells--center">
          {cells.map((c, i) => (
            <span
              key={i}
              className={[
                "t9-cell",
                c === "green" && "t9-cell--green",
                c === "orange" && "t9-cell--orange",
              ]
                .filter(Boolean)
                .join(" ")}
            />
          ))}
        </div>

        <p className="t9-reviewHint">
          در صورت ندانستن معنی واژه، معنی در اینجا قرار می‌گیرد.
        </p>

        <div className="t9-reviewNav">
          <button
            className="t9-pillBtn"
            disabled={index === 0}
            onClick={() => setIndex((i) => i - 1)}
          >
            کلمه قبلی
          </button>


          <button
            className="t9-pillBtn"
            disabled={index === words.length - 1}
            onClick={() => setIndex((i) => i + 1)}
          >
            کلمه بعدی
          </button>
        </div>
      </section>
    </div>
  );
}
