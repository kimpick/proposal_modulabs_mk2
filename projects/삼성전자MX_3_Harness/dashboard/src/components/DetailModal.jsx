import React, { useEffect } from 'react';
import { X, Target, Info, CheckCircle2 } from 'lucide-react';

const DetailModal = ({ item, onClose }) => {
  // Prevent body scroll when modal is open
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, []);

  if (!item) return null;

  return (
    <div 
      style={{
        position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.6)', backdropFilter: 'blur(8px)',
        zIndex: 1000, display: 'flex', justifyContent: 'center', alignItems: 'center',
        padding: '20px'
      }}
      onClick={onClose}
    >
      <div 
        className="glass-panel"
        style={{
          width: '100%', maxWidth: '800px', maxHeight: '90vh',
          backgroundColor: 'rgba(11, 15, 25, 0.85)',
          overflowY: 'auto', padding: '0', display: 'flex', flexDirection: 'column'
        }}
        onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
      >
        {/* Header */}
        <div style={{ padding: '24px', borderBottom: '1px solid var(--card-border)', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <span style={{ fontSize: '0.9rem', color: 'var(--primary-color)', fontWeight: 'bold' }}>
              {item.month} ({item.info?.target === '전직원' ? '공통' : item.type === 'Developer' ? '개발자' : '비개발자'}) - {item.info?.ax_stage || ''}
            </span>
            <h2 style={{ fontSize: '1.8rem', margin: '8px 0', color: '#fff' }}>{item.title}</h2>
            <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', margin: 0 }}>{item.subtitle}</p>
          </div>
          <button onClick={onClose} className="glass-button" style={{ padding: '8px', border: 'none' }}>
            <X size={24} />
          </button>
        </div>

        {/* Body */}
        <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
          
          <section>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#fff', fontSize: '1.3rem', marginBottom: '16px' }}>
              <Info size={20} color="var(--primary-color)"/> 교육 내용
            </h3>
            <div style={{ lineHeight: '1.6', color: 'var(--text-secondary)' }} dangerouslySetInnerHTML={{ __html: item.intro?.replace(/\n/g, '<br/>') || '' }} />
          </section>

          <section>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#fff', fontSize: '1.3rem', marginBottom: '16px' }}>
              <Target size={20} color="var(--accent)"/> 학습 목표
            </h3>
            <div style={{ background: 'rgba(16, 185, 129, 0.1)', borderLeft: '4px solid var(--accent)', padding: '16px', borderRadius: '4px', color: '#f8fafc', lineHeight: '1.6' }}>
              {item.objective}
            </div>
          </section>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
            <section>
              <h4 style={{ color: '#fff', marginBottom: '12px' }}>기술 스택</h4>
              <ul style={{ margin: 0, paddingLeft: '20px', color: 'var(--text-secondary)', lineHeight: 1.8 }}>
                {item.tech_stack?.map((tech, i) => (
                  <li key={i}>{tech}</li>
                ))}
              </ul>
            </section>
            <section>
              <h4 style={{ color: '#fff', marginBottom: '12px' }}>인프라 현황</h4>
              <ul style={{ margin: 0, paddingLeft: '20px', color: 'var(--text-secondary)', lineHeight: 1.8 }}>
                {item.infrastructure?.map((infra, i) => (
                  <li key={i}>{infra}</li>
                ))}
              </ul>
            </section>
          </div>

          <section>
            <h3 style={{ color: '#fff', fontSize: '1.3rem', borderBottom: '1px solid var(--card-border)', paddingBottom: '12px', marginBottom: '16px' }}>커리큘럼 모듈</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {item.modules?.map((mod, i) => (
                <div key={i} style={{ background: 'rgba(255,255,255,0.03)', borderRadius: '12px', padding: '16px', border: '1px solid rgba(255,255,255,0.05)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <h5 style={{ fontSize: '1.1rem', color: '#fff', margin: 0 }}>
                      <span style={{ color: 'var(--primary-color)', marginRight: '8px' }}>Module {mod.module_id}</span>
                      {mod.module_name}
                    </h5>
                    <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{mod.duration}</span>
                  </div>
                  <span style={{ display: 'inline-block', fontSize: '0.8rem', background: 'rgba(255,255,255,0.1)', padding: '2px 8px', borderRadius: '4px', marginBottom: '12px' }}>
                    {mod.subtitle}
                  </span>
                  <ul style={{ margin: 0, paddingLeft: '20px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                    {mod.items?.map((itemLine, idx) => (
                      <li key={idx} style={{ marginBottom: '4px' }}>{itemLine}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>

          {(item.output || item.schedule_message) && (
            <section style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {item.output && (
                <div style={{ background: 'rgba(155, 81, 224, 0.1)', border: '1px solid rgba(155, 81, 224, 0.3)', padding: '16px', borderRadius: '12px'}}>
                  <h4 style={{ color: '#c084fc', margin: '0 0 12px 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <CheckCircle2 size={18} /> 산출물
                  </h4>
                  <div style={{ color: 'var(--text-primary)', '& ul': { margin: 0, paddingLeft: '20px' } }} dangerouslySetInnerHTML={{ __html: item.output }} />
                </div>
              )}
              {item.schedule_message && (
                <div style={{ background: 'rgba(255, 255, 255, 0.05)', padding: '16px', borderRadius: '12px', fontSize: '0.9rem', color: 'var(--text-secondary)' }} dangerouslySetInnerHTML={{ __html: item.schedule_message }} />
              )}
            </section>
          )}

        </div>
      </div>
    </div>
  );
};

export default DetailModal;
