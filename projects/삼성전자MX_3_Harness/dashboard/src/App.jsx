import React, { useState, useEffect } from 'react';
import { loadCurriculums } from './utils/dataLoader';
import CurriculumCard from './components/CurriculumCard';
import DetailModal from './components/DetailModal';
import { Layers, Search, Briefcase, Code } from 'lucide-react';
import './App.css';

function App() {
  const [curriculums, setCurriculums] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [filterMonth, setFilterMonth] = useState('All'); // 'All', '4월', '5월'

  useEffect(() => {
    try {
      const data = loadCurriculums();
      setCurriculums(data);
    } catch (error) {
      console.error("Failed to load curriculums:", error);
    }
  }, []);

  const filteredCurriculums = curriculums.filter(item => {
    if (filterMonth === 'All') return true;
    return item.month === filterMonth;
  });

  return (
    <div style={{ padding: '40px 24px', maxWidth: '1280px', margin: '0 auto' }}>
      {/* Header Area */}
      <header style={{ marginBottom: '48px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', flexWrap: 'wrap', gap: '24px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
            <div style={{ background: 'var(--primary-color)', padding: '12px', borderRadius: '12px', display: 'flex' }}>
              <Layers color="#fff" size={28} />
            </div>
            <div>
              <h1 style={{ fontSize: '2rem', color: '#fff', margin: 0 }}>하네스 엔지니어링 대시보드</h1>
              <p style={{ color: 'var(--text-secondary)', margin: '4px 0 0 0' }}>삼성전자 MX사업부 AI 교육 커리큘럼</p>
            </div>
          </div>
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', gap: '12px', background: 'rgba(255,255,255,0.03)', padding: '8px', borderRadius: '16px', border: '1px solid rgba(255,255,255,0.05)' }}>
          <button 
            className={`glass-button ${filterMonth === 'All' ? 'active' : ''}`}
            onClick={() => setFilterMonth('All')}
          >
            <Search size={16} /> 전체 보기
          </button>
          <button 
            className={`glass-button ${filterMonth === '4월' ? 'active' : ''}`}
            onClick={() => setFilterMonth('4월')}
            style={filterMonth === '4월' ? { background: 'rgba(47, 128, 237, 0.2)', borderColor: 'rgba(47, 128, 237, 0.4)' } : {}}
          >
            <Code size={16} /> 4월 (개발자)
          </button>
          <button 
            className={`glass-button ${filterMonth === '5월' ? 'active' : ''}`}
            onClick={() => setFilterMonth('5월')}
            style={filterMonth === '5월' ? { background: 'rgba(155, 81, 224, 0.2)', borderColor: 'rgba(155, 81, 224, 0.4)' } : {}}
          >
            <Briefcase size={16} /> 5월 (비개발자)
          </button>
        </div>
      </header>

      {/* Grid Area */}
      <main>
        {filteredCurriculums.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '64px', color: 'var(--text-secondary)' }}>
             데이터가 없습니다.
          </div>
        ) : (
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', 
            gap: '24px' 
          }}>
            {filteredCurriculums.map(item => (
              <CurriculumCard 
                key={item.id} 
                item={item} 
                onClick={setSelectedItem} 
              />
            ))}
          </div>
        )}
      </main>

      {/* Detail Modal */}
      {selectedItem && (
        <DetailModal 
          item={selectedItem} 
          onClose={() => setSelectedItem(null)} 
        />
      )}
    </div>
  );
}

export default App;
