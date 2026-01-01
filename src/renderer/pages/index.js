// pages/index.js
import { useState } from "react";

export default function Home() {
  const [fanpageLink, setFanpageLink] = useState("");
  const [postLinks, setPostLinks] = useState("");
  const [numPosts, setNumPosts] = useState(1);
  const [result, setResult] = useState(null);

  const handleRunBot = async () => {
    // Đã thay đổi cổng backend từ 5000/6000 sang 7000
    const res = await fetch("http://127.0.0.1:7000/run-bot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        fanpage_link: fanpageLink,
        post_links: postLinks.split("\n").filter(l => l.trim() !== ""),
        num_posts: numPosts
      })
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Facebook Auto Bot 🤖</h1>
      <input
        placeholder="Fanpage link"
        value={fanpageLink}
        onChange={(e) => setFanpageLink(e.target.value)}
        style={{ width: "100%", marginBottom: 10 }}
      />
      <textarea
        placeholder="Post links (mỗi dòng 1 link)"
        value={postLinks}
        onChange={(e) => setPostLinks(e.target.value)}
        rows={4}
        style={{ width: "100%", marginBottom: 10 }}
      />
      <input
        type="number"
        min="1"
        value={numPosts}
        onChange={(e) => setNumPosts(parseInt(e.target.value))}
        style={{ marginBottom: 10 }}
      />
      <br />
      <button onClick={handleRunBot}>Run Bot</button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <p>{result.message}</p>
          {/* Đã thay đổi cổng backend từ 5000/6000 sang 7000 cho ảnh chụp màn hình */}
          {result.screenshots?.map((img, i) => (
            <img key={i} src={`http://127.0.0.1:7000/${img}`} alt={`screenshot-${i}`} style={{ maxWidth: "100%" }} />
          ))}
        </div>
      )}
    </div>
  );
}