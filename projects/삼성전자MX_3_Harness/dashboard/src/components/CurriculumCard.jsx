import React from 'react';
import { Calendar, Users, Clock, ArrowRight } from 'lucide-react';

const CurriculumCard = ({ item, onClick }) => {
  return (
    <div 
      className="glass-panel" 
      style={{ padding: '24px', cursor: 'pointer', display: 'flex', flexDirection: 'column', gap: '16px', transition: 'transform 0.2s', height: '100%' }}
      onClick={() => onClick(item)}
      onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-4px)'}
      onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <span style={{ 
          background: item.month === '4월' ? 'rgba(47, 128, 237, 0.2)' : 'rgba(155, 81, 224, 0.2)', 
          color: item.month === '4월' ? '#60a5fa' : '#c084fc',
          padding: '4px 8px', borderRadius: '6px', fontSize: '0.8rem', fontWeight: 'bold' 
        }}>
          {item.month} ({item.type === 'Developer' ? '개발자' : '비개발자'})
        </span>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', background: 'rgba(255,255,255,0.05)', padding: '4px 8px', borderRadius: '6px' }}>
          {item.info?.ax_stage || 'N/A'}
        </span>
      </div>
      
      <div>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '8px', color: 'var(--text-primary)' }}>{item.title}</h3>
        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', margin: 0, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
          {item.subtitle}
        </p>
      </div>

      <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div style={{ display: 'flex', gap: '16px', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Users size={14} />
            <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: '120px' }}>{item.info?.target || '전직원'}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Clock size={14} />
            <span>{item.info?.duration || '1일'}</span>
          </div>
        </div>
        
        <button className="glass-button" style={{ justifyContent: 'center', marginTop: '8px' }}>
          상세 보기 <ArrowRight size={16} />
        </button>
      </div>
    </div>
  );
};

export default CurriculumCard;
