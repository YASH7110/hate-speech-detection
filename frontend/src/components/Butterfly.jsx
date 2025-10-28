import React from 'react';
import '../styles/butterfly.css';

const Butterfly = ({ style }) => {
  return (
    <div className="butterfly" style={style}>
      <div className="butterfly-body">
        <div className="butterfly-antenna butterfly-antenna-left"></div>
        <div className="butterfly-antenna butterfly-antenna-right"></div>
      </div>
      <div className="butterfly-wing butterfly-wing-left"></div>
      <div className="butterfly-wing butterfly-wing-right"></div>
    </div>
  );
};

const ButterflyGarden = ({ count = 8 }) => {
  const butterflies = Array.from({ length: count }, (_, i) => ({
    id: i,
    top: `${Math.random() * 80}%`,
    left: `${Math.random() * 90}%`,
    delay: `${Math.random() * 5}s`,
  }));

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden">
      {butterflies.map((butterfly) => (
        <Butterfly
          key={butterfly.id}
          style={{
            top: butterfly.top,
            left: butterfly.left,
            animationDelay: butterfly.delay,
          }}
        />
      ))}
    </div>
  );
};

export default ButterflyGarden;
