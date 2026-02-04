
import { useMemo, useState } from "react";
import MicroserviceCard from "../components/MicroserviceCard";
import { microservices as initialData } from "../services/mockMicroservices";
import { Link } from "react-router-dom";

export default function Microservices() {
  const [q, setQ] = useState("");
  const [items, setItems] = useState(initialData);
  const [editingId, setEditingId] = useState(null);

  const filtered = useMemo(() => {
    const s = q.trim();
    if (!s) return items;
    return items.filter((x) => x.title.includes(s));
  }, [q, items]);

  const addLesson = () => {
    if (editingId) return;

    const newId = Date.now();
    const newItem = {
      id: newId,
      title: "",
      words: 0,
      progress: 0,
    };

    setItems((prev) => [newItem, ...prev]);
    setEditingId(newId);
  };

  const commitTitle = (id, value) => {
    const v = value.trim();

    if (!v) {
      
      setItems((prev) => prev.filter((x) => x.id !== id));
    } else {
      setItems((prev) => prev.map((x) => (x.id === id ? { ...x, title: v } : x)));
    }

    setEditingId(null);
  };

  return (
    <div className="t9-page" dir="rtl" lang="fa">
      <header className="t9-topbar">
        <button className="t9-pillBtn">حساب کاربری</button>
        <h1 className="t9-title">یادگیری مستمر با Tick 8</h1>
        <button className="t9-pillBtn">خانه</button>
      </header>

      <section className="t9-panel">
        <div className="t9-searchRow">
          <span className="t9-searchIcon" aria-hidden="true">
            🔍
          </span>
          <input
            className="t9-search"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="جستجو"
          />
        </div>

        <div className="t9-grid">
          {filtered.map((m) => {
            const isEditing = editingId === m.id;

            return (
              <MicroserviceCard
                key={m.id}
                id={m.id}
                disableNav={isEditing} 
                title={m.title || "نام را وارد کنید"}
                titleNode={
                  isEditing ? (
                    <input
                      autoFocus
                      placeholder="نام را وارد کنید"
                      defaultValue={m.title || ""}
                      onClick={(e) => e.stopPropagation()}
                      onBlur={(e) => commitTitle(m.id, e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === "Enter") e.currentTarget.blur();
                        if (e.key === "Escape") {
                         
                          if (!m.title) {
                            setItems((prev) => prev.filter((x) => x.id !== m.id));
                          }
                          setEditingId(null);
                        }
                      }}
                    />
                  ) : null
                }
                words={m.words}
                progress={m.progress}
                onDelete={() => setItems((prev) => prev.filter((x) => x.id !== m.id))}
              />
            );
          })}
        </div>

        <div className="t9-actions">
          <Link className="t9-actionBtn" to="/add-word">
            افزودن واژه
          </Link>
          <button className="t9-actionBtn" onClick={addLesson}>
            افزودن درس
          </button>
        </div>
      </section>
    </div>
  );
}
