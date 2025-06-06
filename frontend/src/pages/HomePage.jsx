import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="bg-light" style={{ minHeight: '100vh' }}>
      <header className="py-5 text-center bg-primary text-white">
        <h1 className="display-5 fw-bold">سامانه طرح توجیهی آنلاین</h1>
        <p className="lead">به‌سادگی طرح توجیهی خود را بسازید، محاسبات مالی را آنی ببینید و گزارش PDF بگیرید.</p>
        <Link to="/projects/new" className="btn btn-lg btn-light mt-3">
          شروع کنید
        </Link>
      </header>

      <section className="container py-5">
        <h2 className="mb-4 text-center">مراحل کار</h2>
        <div className="row g-4">
          <div className="col-md-4 text-center">
            <h3>۱. ایجاد پروژه</h3>
            <p>عنوان و شرح مختصری برای پروژه خود وارد کنید.</p>
          </div>
          <div className="col-md-4 text-center">
            <h3>۲. ورود داده‌های مالی</h3>
            <p>جداول هزینه، درآمد و جریان نقدی را به‌صورت مرحله‌ای تکمیل کنید.</p>
          </div>
          <div className="col-md-4 text-center">
            <h3>۳. دانلود گزارش</h3>
            <p>پس از ورود، گزارش PDF رسمی همراه شاخص‌های NPV/IRR را دریافت کنید.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default HomePage; 